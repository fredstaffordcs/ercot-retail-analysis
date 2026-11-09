# Sources

All sources are public. Raw downloads are not stored in this repository (about 800 MB); the extracts used are in `data/source_extracts/`.

| Source | Used for | Where to get it |
|---|---|---|
| EIA Form 861 (annual, 1990–2025), Historical and Operational data | Revenue, sales and customers by utility and class; bundled prices; delivery-only data from 2020 | https://www.eia.gov/electricity/data/eia861/ |
| FERC Form 1 (via PUDL) | Wires-company revenue, 1994–2019; functional cost of service 1994–2001 | https://catalyst.coop/pudl/ and https://www.ferc.gov/ferc-online/ferc-online/ferc-form-1 |
| EIA-0437, *Financial Statistics of Major U.S. Investor-Owned Electric Utilities* | Functional cost of service, 1992–93 | EIA publications archive |
| SEC filings (10-K, 8-K, 10-D) of Oncor, CenterPoint, AEP Texas, TNMP and their bond companies | Delivery revenue, bond charges and collections | https://www.sec.gov/edgar |
| PUCT dockets, tariffs, TCRF petitions, rate summaries; ERCOT postage-stamp matrices | Transmission rates and allocation factors, riders, billed rates | https://interchange.puc.texas.gov/ |
| PUCT retail market Market Share Data | Residential MWh and customers by TDU area | https://www.puc.texas.gov/industry/electric/reports/ |
| AEP Texas earnings monitoring reports (16 TAC §25.73), bond servicer reports | AEP delivery and bond charges | PUCT filings (Project numbers in the line items) and EDGAR |
| ERCOT State of the Market reports (Potomac Economics) | All-in wholesale cost per MWh | https://www.potomaceconomics.com/markets-monitored/ercot/ |
| BLS CPI-U | Real-dollar conversion | https://www.bls.gov/cpi/ |
| Press reports (Corpus Christi *Caller-Times*, Dec. 2006; San Angelo *Standard-Times*, Oct. 2, 2006) | AEP clawback amounts and interim credit confirmation | Newspaper archives |

Document-level references (docket numbers, 10-K years, workpaper names) are in the `source`, `source_detail` and `method` columns of the data files and in the line-item files.
