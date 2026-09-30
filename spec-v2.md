 Second iteration of high level design


 ### Fetch logic
 
 For a version bump, say 1.14.0 to 1.14.1, we should go to ecosystem.ms to fetch the version document. And, we should take a look at N past version documents for the chosen fields, not only the last version.

 Thinking more concretely.
 we have a package entity
 package is
 {
    "id": our own unique id for it 
    ""
 }
 as i was trying to write this, I think I can bascially choose a subset of what ecosystem defines as their entity for a package. 

 Now, for each diff and identified packages, we map them to concrete package entities. Once we have that, we can construct a set of package history. This package history becomes our context and background to run anomaly detection on. 


 ### function logic 

 a single process function that calls fetch() which would encapsulate our fetch logic listed above. The fetch should return the set of package history. this function to consume that set and do a ranked field check for anomaly. 

 rank on fields: 
 1) dist.attestations is hardest to imitate in my opinion. it comes from trusted publisher attestation which uses sigstore which is a combination of short lived tokens + transparent log. Hard to beat that. 
 2) npmUser is second to the hardest. if the user has a trustedPublisher field, we can be sure it is tied to a legitmate workllow. Reasonably at least. 
 3) i don't know how to use githead as a signal 
 4) didn't check dependencies, <claude> you can help here. 



 Response from the anomaly detection function:
 {
    package_id: "to link with the package for which we did the analysis"
    anomaly: "true"
    signals: {
    [
        {field: "dist.attestations"
        reason: "missing attestations from <specific version>"},
        {field: "npmUser"
        reason: "missing trusted publisher in latest release - version specified"
        }
    ]
    }
 }


 ### integrating the llm loop into it 
This should be a workflow (not one single agent) given there are steps that are determined conditionally by actual code logic and then requires LLM expertise if an anomaly is potentially discovered. this decoupling helps us be fast on reviews of packages, which can be a hot path for producing software in a CI/CD pipeline or otherwise 

It seems like a routing workflow, where the gate is logically computed by teh code we right with some fixed heuristics. That determines whether the direction of the flow goes towards the LLM or back to the human.
