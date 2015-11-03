#Elasticsearch

## /_cat

The `_cat` endpoint allows to monitor health and get statistics about the cluster.


We can get the health as follows.

	curl http://localhost:9200/_cat/health

We can ask how many documents are in the cluster

	curl http://localhost:9200/_cat/count

and we can get details about shards

	curl http://localhost:9200/_cat/shards

You can get list of all available `_cat` commands as follows

	curl http://localhost:9200/_cat/

## Create Index

Create index with the name `feeds`

	curl -XPOST http://localhost:9200/feeds

Now if we do,

	curl http://localhost:9200/_cat/indices\?v

We should see that index that we just created.

## Creating a type and document

Let's index a feed document. We can assume that this document is being posting to our API. The document has the following format

	{
		wall_id: id of the wall,
		author_id: id of the author,
		post_id: id of the post,
		content: user content,
		created: date,
		like_counter: 0
	}

In ElasticSearch documents are stored as JSON documents and we index them by posting them to the ElasticSearch API.

	curl -XPOST http://localhost:9200/feeds/feed/dcbf514dfbb5a431213cacd977944329c219811e -d '{
		"wall_id": "6b8c53816814712c590debffbd65c50dc33d7745",
		"author_id": "d5ab5f9b33297004bdb577a6455a3b84da3b193f",
		"post_id": "dcbf514dfbb5a431213cacd977944329c219811e",
		"content": "Hello ElasticSearch",
		"created": "2015-10-28T14:12:12",
		"like_counter": 0
	}'

When we did this, we created a new type, namely feed, within the feeds index.

ElasticSearch automatically creates a mapping for the new type. We can see that mapping with

	curl http://localhost:9200/feeds/feed/_mapping?pretty=true

When new documents are added to the type, ElasticSearch parses the document using this mapping. You can change the mapping if you want to treat some fields differently.

We can ask ElasticSearch how many documents a given index contains

	λ ~/ curl http://localhost:9200/_cat/count/feeds\?v
	epoch      timestamp count
	1446142126 18:08:46  1

We can fetch this document by the id as follows

	curl http://localhost:9200/feeds/feed/dcbf514dfbb5a431213cacd977944329c219811e\?pretty\=true

Note that ElasticSearch is near real-time. Thus it might take up to a second for the document to be fully index.

## Updating document

There are two ways to update an indexed document. We can repost the whole document using the same url.

	curl -XPOST http://localhost:9200/feeds/feed/dcbf514dfbb5a431213cacd977944329c219811e -d '{
		"wall_id": "6b8c53816814712c590debffbd65c50dc33d7745",
		"author_id": "d5ab5f9b33297004bdb577a6455a3b84da3b193f",
		"post_id": "dcbf514dfbb5a431213cacd977944329c219811e",
		"content": "Hello ElasticSearch",
		"created": "2015-10-28T14:12:12",
		"like_counter": 1
	}'

When this command is executed we see that the document version has been updated.

	{"_index":"feeds","_type":"feed","_id":"dcbf514dfbb5a431213cacd977944329c219811e","_version":2,"created":false}

The second way to update a given document is by using the `_update` endpoint on a given document. With that endpoint we can partially update the document by sending only the fields we are interested in updating.

	curl -XPOST http://localhost:9200/feeds/feed/dcbf514dfbb5a431213cacd977944329c219811e/_update -d '{
		"doc": {
			"like_counter": 2
		}
	}'

You can also run scripts when updating a given document as can be shown in [https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html)

## Deleting documents and indexes

We can delete documents as follows

	curl -XPOST http://localhost:9200/feeds/feed/dcbf514dfbb5a431213cacd977944329c219811e

We can also delete all documents under a given type

	curl -XPOST http://localhost:9200/feeds/feed

and we can also delete the whole index

	curl -XPOST http://localhost:9200/feeds/

## The search API and the query DSL

For this part lets add some documents that we can play with.

We will have two walls.

- `32f39757ed18dec1864c7409e58afac07bf718b4`
-`4d467f07a5866d0b898ad659437893de69e5e2a0`

and the following two users
- `38170c08cb458fd4879c34b6f608294c50312bbb`
- `ab1b6377aee3209d9d487526a5172b51bba8504c`

Now let's create some data to play with.

	curl -XPOST http://localhost:9200/feeds/feed/1825b7cc1ce5add7fead59e46721d015c5f26e20 -d '{
		"wall_id": "32f39757ed18dec1864c7409e58afac07bf718b4",
		"author_id": "38170c08cb458fd4879c34b6f608294c50312bbb",
		"post_id": "dcbf514dfbb5a431213cacd977944329c219811e",
		"content": "Had dinner with my friends it was great",
		"created": "2014-02-10T14:12:12",
		"like_counter": 23
	}'

	curl -XPOST http://localhost:9200/feeds/feed/583c929c02042b98cb33287c318a070c4b90a43d -d '{
		"wall_id": "32f39757ed18dec1864c7409e58afac07bf718b4",
		"author_id": "ab1b6377aee3209d9d487526a5172b51bba8504c",
		"post_id": "dcbf514dfbb5a431213cacd977944329c219811e",
		"content": "Why didnt Frodo just give the ring to Sauron?",
		"created": "2015-02-14T10:22:03",
		"like_counter": 4
	}'

	curl -XPOST http://localhost:9200/feeds/feed/b8601b95a2aa92eafcef9ea5173bd3f3f87d599c -d '{
		"wall_id": "4d467f07a5866d0b898ad659437893de69e5e2a0",
		"author_id": "38170c08cb458fd4879c34b6f608294c50312bbb",
		"post_id": "dcbf514dfbb5a431213cacd977944329c219811e",
		"content": "Is there any way to handle exceptions without using try and catch?",
		"created": "2015-04-02T13:24:14",
		"like_counter": 79
	}'

To search we use the `_search` endpoint. That endpoint is available over indices and types. We can also apply the search over the whole cluster.

We can both place queries into the query parameter or in a body with using a POST method.

	curl http://localhost:9200/feeds/feed/_search?q="handle"

We can also do the same query with post

	curl -XPOST http://localhost:9200/feeds/feed/_search -d '{
		"query": { "match_all": {} }
	}'

In this example we are applying a [match_all](https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-match-all-query.html) query. This query will simply match all documents found.

We can also do a [match](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html)

	curl -XPOST http://localhost:9200/feeds/feed/_search -d '{
		"query": {
			"match": {
				"wall_id": "32f39757ed18dec1864c7409e58afac07bf718b4"
			}
		}
	}'

This query will give us all documents that have a certain wall_id set to a specific value.

We can also combine multiple match queries with a [bool query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html).

	curl -XPOST http://localhost:9200/feeds/feed/_search -d '{
		"query":{
			"bool": {
				"must": [
					{"match": {"wall_id": "32f39757ed18dec1864c7409e58afac07bf718b4"}},
					{"match": {"author_id": "ab1b6377aee3209d9d487526a5172b51bba8504c"}}
				]
			}
		}
	}'

We can apply filters on the result set. For instance, lets fetch all all feeds for a given wall and filter it on a given range.

	curl -XPOST http://localhost:9200/feeds/feed/_search -d '{
    "query":{

      "bool": {
        "must":
          {"match": {"wall_id": "32f39757ed18dec1864c7409e58afac07bf718b4"}},
        "filter": {
          "range": {
            "created": {
               "gte": "2015-01-01T00:00:00"
            },
            "like_counter": {
              "gte": 4
            }
          }
        }
      }
    }
  }'




