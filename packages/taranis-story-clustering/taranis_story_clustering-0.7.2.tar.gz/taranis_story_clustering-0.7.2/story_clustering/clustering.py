import torch
from sentence_transformers import util
from .document_representation import Keyword, Document, Corpus
from .event_organizer import Event
from .eventdetector import extract_events_from_corpus, SimilarityThreshold
from .keywords_organizer import KeywordGraph, KeywordEdge, KeywordNode
from .nlp_utils import compute_tf, replace_umlauts_with_digraphs
from story_clustering import sentence_transformer, logger


HIGH_PRIORITY = 10
MID_HIGH_PRIORITY = 8
MID_PRIORITY = 5
MID_LOW_PRIORITY = 3
LOW_PRIORITY = 1




def create_corpus(new_news_items: list[dict]) -> Corpus:
    """Creates a Corpus object from a JSON object denoting all documents

    Args:
        new_news_items (list[dict]): list of dict with following keys
            {'id': str, 'link': str, 'text': str, 'title':str,'date': 'YYYY-MM-DD', 'lang': str,
            'tags': [{'name': str, 'tag_type': str}]}
    Returns:
        corpus: Corpus of documents
    """
    corpus = Corpus()
    for nitem_agg in new_news_items:
        doc = Document(doc_id=nitem_agg["id"]) # updated to use aggregate_id
        for nitem in nitem_agg["news_items"]:
            
            doc.url = nitem.get("news_item_data.link", None)
            doc.content = nitem["news_item_data"]["content"] or nitem["news_item_data"]["review"]
            if not doc.content:
                continue
            doc.title = nitem["news_item_data"]["title"]
            if doc.title is not None:
                doc.segTitle = doc.title.strip().split(" ")
            doc.publish_time = nitem.get("news_item_data.published", None)
            doc.language = nitem["news_item_data"]["language"]
            keywords = {}
            if len(nitem_agg["tags"]) < 5:
                continue
            for tag in nitem_agg["tags"].values():
                # print(tag["name"])
                if (tag["name"] not in doc.content):
                    continue
                baseform = replace_umlauts_with_digraphs(tag["name"])
                keyword = Keyword(baseform=baseform, tf=tag.get("tf", 0), df=tag.get("df", 0), documents=set())
                keywords[baseform] = keyword
                
                keyword.tf = compute_tf_with_boost(baseform, doc.content, tag_type=tag.get("type", None))
                
            doc.keywords = keywords
            corpus.docs[doc.doc_id] = doc

    corpus.update_df()
    logger.debug(f"Corpus size: {len(corpus.docs)}")
    return corpus

def compute_tf_with_boost(baseform, content, tag_type) -> int:
    # initialize the term frequency so that special keywords are more relevant
    tf = 0
    if tag_type == "APT" or tag_type == "cves" :
        tf = HIGH_PRIORITY
    elif  tag_type == "Company" or tag_type == "sha256s" or tag_type == "sha1s"  or tag_type == "registry_key_paths" or tag_type == "md5s" \
        or tag_type == "bitcoin_addresses":
        tf = MID_HIGH_PRIORITY
    elif tag_type == "Country" or tag_type == "CVE_VENDOR":
        tf = MID_PRIORITY
    elif tag_type == "PER" or tag_type == "LOC" or tag_type == "ORG":
        tf = MID_LOW_PRIORITY 
    else:
        tf = LOW_PRIORITY
    
    # add the term 
    tf += compute_tf(baseform, content)
    return tf

def initial_clustering(new_news_items: list):
    corpus = create_corpus(new_news_items)

    # stories = cluster_stories_from_events(events)
    # new_aggregates = new_aggregates | to_json_stories(stories)

    events = extract_events_from_corpus(corpus=corpus)
    return to_json_events(events)


def incremental_clustering(new_news_items: list, already_clusterd_events: list):
    corpus = create_corpus(new_news_items)

    # create keyGraph from corpus
    graph = KeywordGraph()
    graph.build_graph(corpus=corpus)

    # add to g the new nodes and edges from already_clusterd_events
    for cluster in already_clusterd_events:
        tags = cluster["tags"]
        for keyword_1 in tags.values():
            for keyword_2 in tags.values():
                if keyword_1 != keyword_2:
                    # doc frequency is the number of documents in the cluster
                    df = len(cluster["news_items"])
                    keyNode1 = get_or_add_keywordNode(keyword_1, graph.graphNodes, df)
                    keyNode2 = get_or_add_keywordNode(keyword_2, graph.graphNodes, df)
                    # add edge and increase edge df
                    update_or_create_keywordEdge(keyNode1, keyNode2)

    # stories = cluster_stories_from_events(events)
    # new_aggregates = new_aggregates | to_json_stories(stories)

    events = extract_events_from_corpus(corpus=corpus, graph=graph)
    return to_json_events(events)


def cluster_stories_from_events(events: list[Event]) -> list[list[Event]]:
    stories = []
    for event in events:
        found_story = False
        for story in stories:
            if belongs_to_story(event, story):
                story.append(event)
                found_story = True
                break
        if not found_story:
            aux = [event]
            stories.append(aux)
    return stories


def to_json_events(events: list[Event]) -> dict:
    all_events = [list(event.docs.keys()) for event in events if event.docs]
    #keywords = [event.keyGraph.graphNodes.keys() for event in events if event.docs]
    return {"event_clusters": all_events} #, "events_keywords":keywords}


def to_json_stories(stories: list[list[Event]]) -> dict:
    # iterate over each story
    # iterate over each event in story
    all_stories = []
    for story in stories:
        s_docs = []
        for event in story:
            s_docs.extend(list(event.docs))
        all_stories.append(s_docs)
    return {"story_clusters": all_stories}


def get_or_add_keywordNode(tag: dict, graphNodes: dict, df: int) -> KeywordNode:
    baseform = replace_umlauts_with_digraphs(tag["name"])
    if baseform in graphNodes:
        node = graphNodes[baseform]
        node.keyword.increase_df(df)
        return node

    keyword = Keyword(baseform=baseform, tf=tag.get("tf", 0), df=tag.get("df", df))
    keywordNode = KeywordNode(keyword=keyword)
    graphNodes[keyword.baseForm] = keywordNode
    return keywordNode


def update_or_create_keywordEdge(kn1: KeywordNode, kn2: KeywordNode):
    edgeId = KeywordEdge.get_id(kn1, kn2)
    if edgeId not in kn1.edges:
        new_edge = KeywordEdge(kn1, kn2, edgeId)
        new_edge.df += 1
        kn1.edges[edgeId] = new_edge
        kn2.edges[edgeId] = new_edge
    else:
        kn1.edges[edgeId].df += 1

        if kn1.edges[edgeId].df != kn2.edges[edgeId].df:
            kn2.edges[edgeId].df = kn1.edges[edgeId].df


def compute_similarity_for_stories(text_1, text_2):
    sent_text_1 = text_1.replace("\n", " ").split(".")
    sent_text_2 = text_2.replace("\n", " ").split(".")

    sent_text_2 = [s for s in sent_text_2 if s != ""]
    sent_text_1 = [s for s in sent_text_1 if s != ""]

    if not sent_text_1 or not sent_text_2:
        return 0

    em_1 = sentence_transformer.encode(sent_text_1, convert_to_tensor=True, show_progress_bar=False)
    em_2 = sentence_transformer.encode(sent_text_2, convert_to_tensor=True, show_progress_bar=False)

    consine_sim_1 = util.pytorch_cos_sim(em_1, em_2)
    max_vals, _inx = torch.max(consine_sim_1, dim=1)
    avg = torch.mean(max_vals, dim=0)
    return avg.item()


def belongs_to_story(ev, story) -> bool:
    text_1 = " ".join([d.title for d in ev.docs.values()])
    text_2 = " ".join([d.title for e in story for d in e.docs.values()])
    return compute_similarity_for_stories(text_1, text_2) >= SimilarityThreshold
