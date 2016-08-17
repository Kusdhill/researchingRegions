### Some interesting genes to look at:
	### APP    - Linked to Alzheimer's Disease
	### BRCA1  - Linked to Breast Cancer
	### BRCA2  - Linked to Breast Cancer
	### HOXB13 - Linked to Prostate Cancer
	### SNCA   - Linked to Parkinson's Disease

### Usage example: http://localhost:5000/gene/BRCA1/term/SO:0001575

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


### pageOneResults returns an un-paginated response if the client would like to see the entire json response
@app.route('/gene/<geneName>/term/<soTerm>')
def pageOneResults(geneName, soTerm):
	pageNumber = 0
	return pagedResults(geneName, soTerm, pageNumber)


### pagedResults returns a paginated response if the result is large and the client would like a bite sized peice of the json response
@app.route('/gene/<geneName>/term/<soTerm>/page/<pageNumber>')
def pagedResults(geneName, soTerm,  pageNumber):
	resultCount = -1
	pageCount = 0

	searchOntologyTerm = str(soTerm)

	### Searches for features by gene symbol
	print("Looking for a gene")
	gene = geneBySymbol(geneName)
	print("Found {}".format(gene.name))
	geneList = []
	geneAndTermDict = {}

	### geneAndTermDict stores the start and endpoints, chromosome reference name, and the term the client would like to search for the given gene 
	geneAndTermDict['name'] = geneName
	geneAndTermDict['start'] = gene.start
	geneAndTermDict['end'] = gene.end
	geneAndTermDict['chrome'] = gene.reference_name.replace('chr','')
	geneAndTermDict['term'] = searchOntologyTerm

	geneList.append(geneAndTermDict)
	geneAndTermDict = {}

	#print(geneList[1]['name'])

	geneIndex = 0


	#print(geneList[0]['name'])

	### Search annotations with feature, range, and effect
	print("searching for variant annotations")
	searchedVarAnns = c.search_variant_annotations(variant_annotation_set_id=functionalAnnotationSet.id, start=gene.start, end=gene.end, reference_name=gene.reference_name.replace('chr',''), effects=[{'id': searchOntologyTerm}])

	variantIdList = []

	### Unpack annotations from the searched variant annotations, and store their ID's in variantIdList 
	print("unpacking annotations and storing ID's")
	for annotation in searchedVarAnns:
		variantIdList.append(annotation.variant_id)
		for teff in annotation.transcript_effects:
			for effect in teff.effects:
				if effect.id==searchOntologyTerm:
					term = effect.term

				#print(annotation)


	#print(variantIdList)

	functionalList = []
	variantList = []

	### Using the ID's in variantIdList, use get_variant function to retrieve start and endpoints and chromosome reference name
	### For every ID in variantIdList, populate functionalDict and then append the dictionary to functionalList
	print("storing start and endpoints for each variant ID")
	for id_ in variantIdList:
		gotten = c.get_variant(id_)
		#print(gotten)
		variantList.append(gotten)
		#print("variantList",variantList)

	
		functionalDict = {}
		functionalDict['start'] = gotten.start
		#print(functionalDict['start'])
		functionalDict['end'] = gotten.end
		functionalDict['term'] = term
		functionalDict['chrome'] = gotten.reference_name
		functionalList.append(functionalDict)


	### Now that we have all of the functional annotation data we need, we need to dig into the phase3-release data
	print("grabbing phase3-releases")
	for variantSet in c.search_variant_sets(dataset.id):
		if variantSet.name == "phase3-release":
			phaseVariantSet = variantSet

	### Grab all 2504 individuals in the ga4gh data set, we will use this to compare to searchResults below
	print("grabbing call sets")
	allCallSets = list(c.search_call_sets(phaseVariantSet.id))
	#print(len(allCallSets))
	#print(allCallSets[0])
	callSetIds = []
	### Store all 2504 call set ID's in the callSetIds list
	for callSet in allCallSets:
		callSetIds.append(str(callSet.id))

	### Using all of the variants within variantList, search for variants based on the start position, end position, and the call set ID's
	### Then, for all of the found results, if the result start, end, and chromosome reference name matches the start, end, and chromosome
	### reference name of the variants in variantList, append it to phaseVariantList
	print("creating phaseVariantList")
	phaseVariantList = []
	for variant in variantList:
		searchResults = c.search_variants(phaseVariantSet.id, start=variant.start, end=variant.end, reference_name=variant.reference_name, call_set_ids=callSetIds)
		for result in searchResults:
			if result.start==variant.start and result.end==variant.end and result.reference_bases==variant.reference_bases:
				phaseVariantList.append(result)
		#print(searchResults)


	matchList = []

	#print(functionalList)
	#print(len(functionalList))

	
	#print(phaseVariantList)

	### If a given callset possesses the search term the user is looking for (if the genotype == 1), then the start point and end point
	### are added to the matchResults dictionary. matchResults is the JSON that will be returned to the client. 
	### A human-friendly string is printed so that the client can easily see where matches were found.
	print("finding matches")
	for variant in phaseVariantList:
		for call in variant.calls:
			if call.genotype[0]==1 or call.genotype[1]==1:
				#print(call.genotype[0], call.genotype[1], unicode(call.call_set_name))
				
				resultCount+=1

				matchResults = {}
				#print(phaseVariantList[i].calls[j])

				print(unicode(call.call_set_name+" has "+str(term)+" in gene "+geneList[geneIndex]['name']+" at position "+str(variant.start)+" to "+str(variant.end)))
				
				bioSamplesList = []
				for callSet in allCallSets:
					if call.call_set_id == callSet.id:
						bioSamplesList.append(c.get_bio_sample(callSet.bio_sample_id))



				for sample in bioSamplesList:
					matchResults['biosample'] 	= p.toJsonDict(sample)
				matchResults['term']   			= term
				matchResults['start']  			= str(variant.start)
				matchResults['end']    			= str(variant.end)
				matchResults['result_number'] 	= resultCount

				if resultCount==100:
					pageCount+=1
					print("100 results")

				#print(matchResults)
				#print(index)
				matchList.append(matchResults)


	return flask.jsonify({'matches' : matchList, 'gene' : geneList[geneIndex]['name']})

if __name__ == '__main__':
	app.debug = True  # helps us figure out if something went wrong
	app.run()         # starts the server and keeps it running