### Some interesting genes to look at:
	### APP    - Linked to Alzheimer's Disease
	### BRCA1  - Linked to Breast Cancer
	### BRCA2  - Linked to Breast Cancer
	### HOXB13 - Linked to Prostate Cancer
	### SNCA   - Linked to Parkinson's Disease

### Usage example:	http://localhost:5000/gene/BRCA1/term/SO:0001630
### or 				http://localhost:5000/gene/BRCA1/term/SO:0001630/page/5

import flask
app = flask.Flask(__name__)
import json

import ga4gh.client as client
import ga4gh.protocol as p


### Initialize the client
c = client.HttpClient("http://1kgenomes.ga4gh.org")
dataset = c.search_datasets().next()

### Get functional-annotation from variant sets, the functional-annotation ID will be used below
for result in c.search_variant_sets(dataset.id):
	if result.name == "functional-annotation":
		functionalVariantSet = result


### functional-annotation id is used to get functional annotation set
functionalAnnotationSet = c.search_variant_annotation_sets(variant_set_id=functionalVariantSet.id).next()
feature_set = c.search_feature_sets(dataset.id).next()


### geneBySymbol function allows client to input a gene symbol so they don't need to remember start and endpoints or chromosome reference name
def geneBySymbol(symbol):
  return c.search_features(feature_set.id, gene_symbol=symbol, feature_types=['gene']).next()


### pageOneResults returns the zeroeth page if the client does not provide a page
@app.route('/gene/<geneName>/term/<soTerm>')
def pageOneResults(geneName, soTerm):
	pageNumber = 0
	return pagedResults(geneName, soTerm, pageNumber)



### pagedResults returns a paginated response, the client provides the page they would like to see
@app.route('/gene/<geneName>/term/<soTerm>/page/<pageNumber>')
def pagedResults(geneName, soTerm,  pageNumber):
	resultCount = 0
	pageSize = 20
	pageCount = 0

	searchOntologyTerm = str(soTerm)

	### Searches for features by gene symbol
	print("Looking for a gene")
	gene = geneBySymbol(geneName)
	print("Found {}".format(gene.name))

	### FUNCTIONAL ANNOTATIONS ###
	### Search annotations with feature, range, and effect
	print("searching for variant annotations")
	searchedVarAnns = c.search_variant_annotations(variant_annotation_set_id=functionalAnnotationSet.id, start=gene.start, end=gene.end, 
		reference_name=gene.reference_name.replace('chr',''), effects=[{'id': searchOntologyTerm}])

	variantIdList = []

	### Unpack annotations from the searched variant annotations, and store their ID's in variantIdList
	### Store the term name in the term variable
	print("unpacking annotations and storing ID's")
	for annotation in searchedVarAnns:
		variantIdList.append(annotation.variant_id)
		for teff in annotation.transcript_effects:
			for effect in teff.effects:
				if effect.id==searchOntologyTerm:
					term = effect.term

	variantList = []



	### Using the ID's in variantIdList, use get_variant function to store the variant information in variantList
	### This will be used later below in a for loop
	print("populating variantList")
	for id_ in variantIdList:
		gotten = c.get_variant(id_)
		variantList.append(gotten)


	### PHASE3-RELEASE ###
	### Now that we have all of the functional annotation data we need, we need to dig into the phase3-release data
	print("grabbing phase3-releases")
	for variantSet in c.search_variant_sets(dataset.id):
		if variantSet.name == "phase3-release":
			phaseVariantSet = variantSet

	### Grab bio sample information of all individuals. This information includes population information and family data
	print("grabbing biosamples")
	bioSampleDict = {}
	bioSamplesList = list(c.search_bio_samples(dataset.id))
	bsIdToBsam = {}
	for biosample in c.search_bio_samples(dataset.id):
		bsIdToBsam[biosample.id] = biosample
	allCallSets = list(c.search_call_sets(phaseVariantSet.id))

	### Store all 2504 call set ID's in the callSetIds list and populate the bioSampleDict object
	print("grabbing callsets")
	callSetIds = []
	for callSet in allCallSets:
		callSetIds.append(str(callSet.id))
		bioSampleDict[callSet.id] = bsIdToBsam[callSet.bio_sample_id]


	### Using all of the variants within variantList, search for variants based on the start position, end position, and the call set ID's
	### If a given callset possesses the search term the client is looking for (if genotype[0]==1), then the result is a match and its information
	### is added to matchList

	### The pagination feature is worked into the for loops as well; If the number of found results are greater than or equal to the number
	### of results per page multiplied by the page the client wants then the result is appended to matchList, otherwise the loops are broken out of.
	print("creating matchList")
	matchList = []
	phaseVariantList = []
	nextPageNum = int(pageNumber)
	for variant in variantList:
		searchResults = c.search_variants(phaseVariantSet.id, start=variant.start, end=variant.end, 
			reference_name=variant.reference_name, call_set_ids=callSetIds)
		for result in searchResults:
			if len(matchList) == pageSize:
				break
			for call in result.calls:
				if call.genotype[0]==1 or call.genotype[1]==1:
					### A human-friendly string is printed so that the client can easily see where matches were found.
					readableString = unicode(call.call_set_name+" has "+str(term)+" in gene "+geneName+" at position "
					 +str(variant.start)+" to "+str(variant.end))
					print(readableString)
					
					matchResult = {}
					v = p.toJsonDict(result)
					del v['calls']
					matchResult['variant'] = v
					matchResult['biosample'] = p.toJsonDict(bioSampleDict[call.call_set_id])

					resultCount += 1
					if len(matchList) == pageSize:
						nextPageNum+=1
						if nextPageNum==int(pageNumber):
							nextPageNum=None
						break
					if resultCount>=(pageSize*int(pageNumber)):
						matchList.append(matchResult)


	### Finally, the next page token, matchList, gene, term, and search ontology term are returned to the client as JSON
	
	print("returning")
	return flask.jsonify({'next_page_token' : nextPageNum, 'matches' : matchList, 'gene' : geneName, 'term' : term, 'search_ontology_term' : soTerm})

if __name__ == '__main__':
	app.debug = True  # helps figure out if something went wrong
	app.run()         # starts the server and keeps it running