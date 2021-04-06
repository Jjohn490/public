query_1 = """
query {
  organization(login: "Org") {
    samlIdentityProvider {
      ssoUrl,
      externalIdentities(first: 50) {
        pageInfo{
            endCursor
            hasNextPage
            hasPreviousPage
            startCursor
        }
        edges {
          node {
            guid,
            samlIdentity {
              nameId
            }
           ...on ExternalIdentity{
            user {
               login
              }
            }
          }
        }
      }
    }
  }
}
"""

query_2 = """
query ($cursor: String) {
  organization(login: "Org") {
    samlIdentityProvider {
      ssoUrl,
      externalIdentities( first: 50, after: $cursor ) {
        pageInfo{
            endCursor
            hasNextPage
            hasPreviousPage
            startCursor
        }
        edges {
          node {
            guid,
            samlIdentity {
              nameId
            }
           ...on ExternalIdentity{
            user {
               login
              }
            }
          }
        }
      }
    }
  }
}
"""
