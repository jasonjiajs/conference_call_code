using CSV
using DataFrames
using SASLib

dfcountry_sas=DataFrame(readsas("C:\\Users\\jasonjia\\Dropbox\\Projects\\ConferenceCall\\Output\\FirmIdentification\\Previous20210924\\country1.sas7bdat"))
CSV.write("C:\\Users\\jasonjia\\Dropbox\\Projects\\ConferenceCall\\Output\\FirmIdentification\\Previous20210924\\countrytest1.csv",dfcountry_sas)
