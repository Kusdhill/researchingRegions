
# coding: utf-8

# In[1]:

import ga4gh.client as client
c = client.HttpClient("http://1kgenomes.ga4gh.org")

import collections


# In[2]:

dataset = c.search_datasets().next()

for functionalVariantSet in c.search_variant_sets(dataset.id):
	if functionalVariantSet.name == "functional-annotation":
		functionalAnnotation = functionalVariantSet

functionalAnnotationSet = c.search_variant_annotation_sets(variant_set_id=functionalAnnotation.id).next()


# In[3]:

geneList = []

geneAndTermDict = collections.OrderedDict()

geneAndTermDict['name'] = 'BRCA1'
geneAndTermDict['start'] = 43044295
geneAndTermDict['end'] = 43170245
geneAndTermDict['chrome'] = '17'
geneAndTermDict['term'] = 'SO:0001630'

geneList.append(geneAndTermDict)


print(geneList[0]['name'])


# In[4]:

"""
positions = True
startPos = 41234400
endPos = 41234420
chrome='17'
"""

searchedVarAnns = c.search_variant_annotations(variant_annotation_set_id=functionalAnnotationSet.id, start=geneList[0]['start'], end=geneList[0]['end'], reference_name=geneList[0]['chrome'], effects=[{'id': geneList[0]['term']}])

	

idList = []
termList = []
for annotation in searchedVarAnns:
	for i in range(0,len(annotation.transcript_effects)):
		for j in range(0,len(annotation.transcript_effects[i].effects)):
			termList.append(annotation.transcript_effects[i].effects[j].term)
			#print(annotation)
			idList.append(annotation.variant_id)

#print(idList)
print(termList)

functionalList = []
for i in range(0,len(idList)):
	gotten = c.get_variant(idList[i])
	functionalDict = collections.OrderedDict()
	
	functionalDict['start'] = gotten.start
	functionalDict['end'] = gotten.end
	functionalDict['term'] = termList[i]
	functionalDict['chrome'] = gotten.reference_name
	
	functionalList.append(functionalDict)
	


#print(functionalDict)
#print(functionalList[0]['start'])


# In[5]:

for phaseVariantSet in c.search_variant_sets(dataset.id):
	if phaseVariantSet.name == "phase3-release":
		phaseAnnotation = phaseVariantSet

allCallSets = list(c.search_call_sets(phaseAnnotation.id))

callSetIds = []
for callSet in allCallSets:
	callSetIds.append(str(callSet.id))

phaseAnnotationSetList = []
for i in range(0,len(functionalList)):
	searchResults = c.search_variants(phaseAnnotation.id, start=functionalList[i]['start'], end=functionalList[i]['end'], reference_name=functionalList[i]['chrome'], call_set_ids=callSetIds)
	for results in searchResults:
		phaseAnnotationSetList.append(results)
		
#print(len(phaseAnnotationSetList))


for i in range(0,len(phaseAnnotationSetList)):
	for j in range(0,len(phaseAnnotationSetList[i].calls)):
		if phaseAnnotationSetList[i].calls[j].genotype[0]==1 or phaseAnnotationSetList[i].calls[j].genotype[1]==1:
			#print(phaseAnnotationSetList[i].calls[j])
		
			print unicode(phaseAnnotationSetList[i].calls[j].call_set_name+" has "+str(termList[i])+" in gene "+geneList[0]['name']+" at position "+str(functionalList[i]['start'])+" to "+str(functionalList[i]['end']))

