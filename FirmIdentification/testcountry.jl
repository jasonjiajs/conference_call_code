using CSV
using DataFrames
using SASLib

dfcountry_sas=DataFrame(readsas("C:\\Users\\jasonjia\\Dropbox\\ConferenceCall\\country1.sas7bdat"))
CSV.write("C:\\Users\\jasonjia\\Dropbox\\ConferenceCall\\countrytest1.csv",dfcountry_sas)
