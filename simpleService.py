import flask
app = flask.Flask(__name__)
import json

import ga4gh.client as client
import ga4gh.protocol as p

c = client.HttpClient("http://1kgenomes.ga4gh.org")
dataset = c.search_datasets().next()

for result in c.search_variant_sets(dataset.id):
	if result.name == "functional-annotation":
		functionalVariantSet = result

functionalAnnotationSet = c.search_variant_annotation_sets(variant_set_id=functionalVariantSet.id).next()


feature_set = c.search_feature_sets(dataset.id).next()

def geneBySymbol(symbol):
  return c.search_features(feature_set.id, gene_symbol=symbol, feature_types=['gene']).next()



@app.route('/gene/<geneName>/term/<soTerm>')
def pageOneResults(geneName, soTerm):
	pageNumber = 0
	return pagedResults(geneName, soTerm, pageNumber)


@app.route('/gene/<geneName>/term/<soTerm>/page/<pageNumber>')
def pagedResults(geneName, soTerm,  pageNumber):
	resultCount = 0
	pageCount = 1

	searchOntologyTerm = str(soTerm)

	# Searching for features by gene symbol
	gene = geneBySymbol(geneName)

	geneList = []
	geneAndTermDict = {}


	geneAndTermDict['name'] = geneName
	geneAndTermDict['start'] = gene.start
	geneAndTermDict['end'] = gene.end
	geneAndTermDict['chrome'] = gene.reference_name.replace('chr','')
	geneAndTermDict['term'] = searchOntologyTerm

	geneList.append(geneAndTermDict)
	geneAndTermDict = {}

	"""
	# Linked to Breast Cancer
		BRCA2

	# Linked to Alzheimer's Disease
		APP

	# Linked to Prostate Cancer
		HOXB13

	# Linked to Parkinson's Disease
		SNCA
	"""

	#print(geneList[1]['name'])

	geneIndex = 0


	#print(geneList[0]['name'])

	# Search annotations with feature, range, and effect
	searchedVarAnns = c.search_variant_annotations(variant_annotation_set_id=functionalAnnotationSet.id, start=gene.start, end=gene.end, reference_name=gene.reference_name.replace('chr',''), effects=[{'id': searchOntologyTerm}])

	variantIdList = []
	termList = []
	for annotation in searchedVarAnns:
		for i in range(0,len(annotation.transcript_effects)):
			for j in range(0,len(annotation.transcript_effects[i].effects)):
				termList.append(annotation.transcript_effects[i].effects[j].term)
				#print(annotation)
				variantIdList.append(annotation.variant_id)

	#print(variantIdList)
	#print("termList",termList)
	#print(len(termList))

	functionalList = []
	variantList = []
	for id_ in variantIdList:
		gotten = c.get_variant(id_)
		variantList.append(gotten)


		functionalDict = {}
		functionalDict['start'] = gotten.start
		#print(functionalDict['start'])
		functionalDict['end'] = gotten.end
		functionalDict['term'] = termList[i]
		functionalDict['chrome'] = gotten.reference_name
		functionalList.append(functionalDict)




	for variantSet in c.search_variant_sets(dataset.id):
		if variantSet.name == "phase3-release":
			phaseVariantSet = variantSet

	allCallSets = list(c.search_call_sets(phaseVariantSet.id))
	#print(allCallSets[0])

	callSetIds = []
	for callSet in allCallSets:
		callSetIds.append(str(callSet.id))


	phaseVariantList = []
	for variant in variantList:
		searchResults = c.search_variants(phaseVariantSet.id, start=variant.start, end=variant.end, reference_name=variant.reference_name, call_set_ids=callSetIds)
		for result in searchResults:
			if result.start==variant.start and result.reference_bases==variant.reference_bases and result.reference_bases==variant.reference_bases:
				phaseVariantList.append(result)


	matchList = []

	#print(functionalList)
	#print(len(functionalList))

	# Find callsets with 'yes' call
	#print(phaseVariantList)

# Fix loop issue here
################################################################################################################################
	for i in range(0,len(phaseVariantList)):
		for j in range(0,len(phaseVariantList[i].calls)):
################################################################################################################################
			if phaseVariantList[i].calls[j].genotype[0]==1 or phaseVariantList[i].calls[j].genotype[1]==1:
				#print(phaseVariantList[i].calls[j].genotype[0],phaseVariantList[i].calls[j].genotype[1])
				
				resultCount+=1

				matchResults = {}
				#print(phaseVariantList[i].calls[j])

				#### fix unnecesary termList issue
				print(unicode(phaseVariantList[i].calls[j].call_set_name+" has "+str(termList[0])+" in gene "+geneList[geneIndex]['name']+" at position "+str(functionalList[i]['start'])+" to "+str(functionalList[i]['end'])))
				
				
				#for ids in callSetIds:
				bioSamplesList = []
				for k in range(0,len(allCallSets)):
					if phaseVariantList[i].calls[j].call_set_id == allCallSets[k].id:
						bioSamplesList.append(c.get_bio_sample(allCallSets[k].bio_sample_id))



				for x in range(0,len(bioSamplesList)):
					matchResults['biosample'] = p.toJsonDict(bioSamplesList[x])
				matchResults['term']   = termList[i]
				matchResults['start']  = str(functionalList[i]['start'])
				matchResults['end']    = str(functionalList[i]['end'])
				matchResults['result_number'] = resultCount

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