from kraken_schema_org.helpers import schema_org_website_data as w


def get_sample_data(record_type):
    """Given a record_type, returns a sample record
    """

    record = {
        "@type": record_type
             }

    keys = w.get_keys(record_type)
    if not keys:
        return None
    
    for i in keys:
        value = get_sample_properties(i)
        if value:
            record[i] = get_sample_properties(i)

    return record

    



def get_sample_properties(property):
    properties = {
        "givenName": "John",
        "familyName": "Smith",
        "telephone": "+15147004400",
        "email": "test@test.com",
        "url": "https://www.test.com/",
        "address": {
            "@type": "postalAddress",
            "streetAddress": "1100 Main St.",
            "addressLocality": "Montreal", 
            "addressRegion": "QC",
            "addressCountry": "CA",
            "postalCode": "J5Y 4B3"
        },
        "worksFor": {
            "@type": "organization",
            "@id": "test_org1",
            "name": "Test organization",
            "url": "https://www.test_organization.com/"
        },
        "title": "Job title",
        "streetAddress": "1100 Main St.",
        "addressLocality": "Montreal", 
        "addressRegion": "QC",
        "addressCountry": "CA",
        "postalCode": "J5Y 4B3",
        "actionStatus": "CompletedActionStatus",
        "instrument": {
            "@type": "WebAPI",
            "url": "https://api.com/",
            "name": "Name of web api"
        },
        "object": {
            "@type": "product",
            "name": "Product being transformed"
        },
        "agent": {
            "@type": "person",
            "givenName": "John",
            "familyName": "Smith"
        },
        "result": {
            "@type": "product",
            "name": "Resulting product"
        },
        "startTime": "2023-01-01T11:00:00Z",
        "endTime": "2023-02-01T13:00:00Z"
    }

    return properties.get(property, None)
    

    