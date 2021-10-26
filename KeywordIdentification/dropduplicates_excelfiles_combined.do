import excel "C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\ConferenceCalls_Combined_v2\entryfiles_combined_v2.xlsx", sheet("Sheet1") firstrow clear

log using "C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\ConferenceCalls_Combined_v2\entryfiles_combined_v2_dropduplicates.smcl", replace

duplicates report
duplicates list
duplicates drop

export excel using "C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\ConferenceCalls_Combined_v2\entryfiles_combined_v2_duplicatesdropped.xlsx", firstrow(variables) replace

log close
