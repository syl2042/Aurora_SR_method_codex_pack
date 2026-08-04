# Findings - SR propagation gate

- Le pack 3.2.2 contient deja `Backlog Mutation Gate`, `Global Impact Gate`, `Lot Completion Gate`, `Verification Gate` et `Self Evaluation Gate`, mais aucun gate explicite ne force la propagation des changements de symboles ou contrats partages.
- Les validateurs existants savent refuser `done` sur couverture de lot incomplete, mais ne savent pas encore refuser un `done` quand un changement de signature ou de nom n'a pas prouve ses consommateurs.
- La migration doit etre additive : rendre les anciens contrats invalides casserait les upgrades des projets SR deja installes.
