# Phase B media-payload closure

Date: 20 August 2026 (Australia/Sydney).

## Outcome

The authorised non-Band-A remediation is implemented in the reproducible derivative pipeline.
The public-media gate improved from **40 failures to 16**. The remaining 16 are exactly the
blank Band A owner verdicts. Their files are held outside the public intake and derivative,
but the gate correctly continues to fail. **Phase B is not complete and no staging import is
authorised.**

```text
  immutable files                         7/7 MATCH
  derivative pages                       75 (81 withdrawn absent)
  derivative attachment records          51 permitted
  manifest                               83 = 51 RENAME + 16 EXCLUDE + 16 HOLD
  remaining Elementor media references  409, all resolved
  D32                                    17 sections / 16 pages / 47 markers removed
  Band B                                 9/9 PASS
  public-media gate                      FAIL — 16 blank Band A verdicts only
  index-ready                            0 of 77
  launch                                 NO-GO
```

The task named Gates 7 and 16, but the exact 40-failure population is from current preflight
**Gate 17**. Gate 7 is uniqueness and Gate 16 is claim-to-evidence. Gate 16 separately held
four Band B REAL_PHOTO_PENDING adjacencies; all four disappeared with their complete D32 modules.

Repository discrepancy: `RUN-BLOCK-02-on-inputs.md` does not exist. The actual
file is `RUN-BLOCK-02.md`; it was read without alteration.

## Ground and reproducibility

`build/46-active-main-import.xml` SHA-256: **`4804CA4E5D2BA23D9AC5CE774454BB4F8ED50E916F6C4090B14F56E5180FDA2B`**.

`build/47-media-remediation.csv` SHA-256: **`067C20884CD4CE2DAA280FF567ADA592CF1E236489B1D87B076E4F6B52959798`**.

The architecture generator rebuilds both files from the immutable WXR and authoritative mutable
inputs. The check mode reproduces them byte-for-byte; the derivative was not manually patched.

## All 40 original assertions

Each row records immutable-WXR page placements and Elementor reference counts. Exact Elementor
paths, widget IDs, URLs and alts are in `reports/47-original-media-blockers.json`.

| # | Class | ID / filename at failure | WXR placements and Elementor references | Final disposition |
|---:|---|---|---|---|
| 1 | denied_asset_remains | 159 `chatgpt-image-jul-6-2026-01-52-19-pm-camden-159.png` | 0 refs / 0 pages; active 0 refs / 0 pages; withdrawn 0 refs / 0 pages. attachment record/file only; no page placement | D24/D36 retired AI/source-brand attachment. Applied: EXCLUDE |
| 2 | denied_asset_remains | 177 `cropped-chatgpt-image-jul-6-2026-07-59-41-pm-camden-177.png` | 0 refs / 0 pages; active 0 refs / 0 pages; withdrawn 0 refs / 0 pages. attachment record/file only; no page placement | D24/D36 retired AI/source-brand attachment. Applied: EXCLUDE |
| 3 | denied_asset_remains | 272 `cropped-chatgpt-image-jul-6-2026-01-52-19-pm-camden-272.png` | 14 refs / 14 pages; active 1 refs / 1 pages; withdrawn 13 refs / 13 pages. /camden-council-driveway-crossing/ (706, draft, withdrawn); /coloured-concrete-driveway-cost/ (1465, draft, withdrawn); /concrete-crossovers-and-laybacks-austral/ (1481, draft, withdrawn); /concrete-crossovers-and-laybacks-currans-hill/ (1496, draft, withdrawn); /concrete-crossovers-and-laybacks-leppington/ (1471, draft, withdrawn); /concrete-crossovers-and-laybacks-oran-park/ (1467, draft, withdrawn); /concrete-crossovers-and-laybacks-south-west-sydney/ (1368, publish, active); /concrete-crossovers-and-laybacks-spring-farm/ (1494, draft, withdrawn); /concrete-driveway-cost-nsw/ (555, draft, withdrawn); /driveway-cost-calculator/ (1457, draft, withdrawn); /exposed-aggregate-driveway-cost/ (1464, draft, withdrawn); /plain-concrete-driveway-cost/ (1463, draft, withdrawn); /slab-volume-calculator/ (1458, draft, withdrawn); /stencilled-concrete-driveway-cost/ (1466, draft, withdrawn) | D24 and C2PA/AI provenance finding. Applied: EXCLUDE |
| 4 | denied_asset_remains | 280 `image-testemonials-camden-280.jpeg` | 14 refs / 14 pages; active 8 refs / 8 pages; withdrawn 6 refs / 6 pages. /commercial-concreting-gregory-hills/ (1474, draft, withdrawn); /concrete-driveway-replacement-south-west-sydney/ (1366, publish, active); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gledswood-hills/ (1476, draft, withdrawn); /concrete-vs-pavers-vs-asphalt/ (1450, draft, withdrawn); /concreters-bradbury/ (1413, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gilead/ (1415, draft, active); /concreters-kemps-creek/ (1403, draft, active); /concreters-mount-annan/ (1375, draft, active); /concreters-tahmoor/ (1419, draft, active); /exposed-aggregate-vs-plain-concrete/ (1461, draft, withdrawn); /liverpool-council-vehicle-crossing/ (1425, draft, withdrawn); /stencilled-vs-stamped-concrete-cost/ (1440, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: EXCLUDE |
| 5 | denied_asset_remains | 306 `corex-concreters-camden-logo-306.png` | 8 refs / 8 pages; active 5 refs / 5 pages; withdrawn 3 refs / 3 pages. /about/ (1364, publish, active); /concrete-patios-edmondson-park/ (1488, draft, withdrawn); /concrete-patios-elderslie/ (1495, draft, withdrawn); /concrete-patios-gledswood-hills/ (1478, draft, withdrawn); /concrete-patios-south-west-sydney/ (195, publish, active); /contact/ (321, publish, active); /gallery/ (1365, publish, active); /quote/ (1363, publish, active) | D18/D36 retired E&T brand attachment. Applied: EXCLUDE |
| 6 | denied_asset_remains | 307 `corex-concreters-camden-logo-307.png` | 2 refs / 2 pages; active 1 refs / 1 pages; withdrawn 1 refs / 1 pages. /concrete-paths-edmondson-park/ (1487, draft, withdrawn); /concrete-paths-south-west-sydney/ (178, publish, active) | D18/D36 retired E&T brand attachment. Applied: EXCLUDE |
| 7 | denied_asset_remains | 308 `corex-concreters-camden-logo-308.png` | 0 refs / 0 pages; active 0 refs / 0 pages; withdrawn 0 refs / 0 pages. attachment record/file only; no page placement | D24 and C2PA/AI provenance finding. Applied: EXCLUDE |
| 8 | denied_asset_remains | 309 `corex-concreters-camden-logo-309.png` | 0 refs / 0 pages; active 0 refs / 0 pages; withdrawn 0 refs / 0 pages. attachment record/file only; no page placement | D24 and C2PA/AI provenance finding. Applied: EXCLUDE |
| 9 | denied_asset_remains | 422 `corex-concreters-camden-logo-422.png` | 0 refs / 0 pages; active 0 refs / 0 pages; withdrawn 0 refs / 0 pages. attachment record/file only; no page placement | D18/D36 retired E&T brand attachment. Applied: EXCLUDE |
| 10 | denied_asset_remains | 469 `corex-concreters-camden-logo-469.png` | 0 refs / 0 pages; active 0 refs / 0 pages; withdrawn 0 refs / 0 pages. attachment record/file only; no page placement | D18/D36 retired E&T brand attachment. Applied: EXCLUDE |
| 11 | denied_asset_remains | 472 `corex-concreters-camden-logo-472.png` | 0 refs / 0 pages; active 0 refs / 0 pages; withdrawn 0 refs / 0 pages. attachment record/file only; no page placement | D18/D36 retired E&T brand attachment. Applied: EXCLUDE |
| 12 | denied_asset_remains | 1067 `verified-badge-e1784545689665-camden-1067.avif` | 14 refs / 14 pages; active 6 refs / 6 pages; withdrawn 8 refs / 8 pages. /coloured-concrete-explained/ (1445, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-catherine-field/ (1485, draft, withdrawn); /concrete-driveways-spring-farm/ (1493, draft, withdrawn); /concrete-slabs-leppington/ (1472, draft, withdrawn); /concreters-camden-south/ (1380, draft, active); /concreters-currans-hill/ (1376, draft, active); /concreters-glen-alpine/ (1414, draft, active); /concreters-leppington/ (221, publish, active); /concreters-narellan/ (1372, draft, active); /concreters-west-hoxton/ (1391, draft, active); /do-i-need-council-approval-driveway-nsw/ (1429, draft, withdrawn); /removing-oil-stains-and-tyre-marks-from-concrete/ (1456, draft, withdrawn); /wollondilly-council-driveway-crossing/ (1427, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: EXCLUDE |
| 13 | band_a_verdict_missing | 907 `camden-town-centre-907.jpg` | 16 refs / 14 pages; active 9 refs / 7 pages; withdrawn 7 refs / 7 pages. /broom-finish-concrete/ (1447, draft, withdrawn); /commercial-concreting-narellan/ (1490, draft, withdrawn); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gregory-hills/ (1475, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gledswood-hills/ (1370, publish, active); /concreters-kirkham/ (1381, draft, active) x2; /concreters-narellan-vale/ (1373, draft, active); /concreters-the-oaks/ (1423, draft, active) x2; /control-joints-and-saw-cut-timing/ (1437, draft, withdrawn); /non-slip-finishes-for-pools-and-slopes/ (1448, draft, withdrawn); /what-actually-moves-a-concrete-quote/ (1443, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 14 | band_a_verdict_missing | 924 `coloured-concrete-south-west-sydney-924.png` | 15 refs / 15 pages; active 8 refs / 8 pages; withdrawn 7 refs / 7 pages. /campbelltown-council-driveway-crossing/ (1426, draft, withdrawn); /commercial-concreting-south-west-sydney/ (1369, publish, active); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gregory-hills/ (1475, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gledswood-hills/ (1370, publish, active); /concreters-len-waters-estate/ (1396, draft, active); /concreters-narellan/ (1372, draft, active); /concreters-theresa-park/ (1384, draft, active); /curing-concrete-in-summer-vs-winter/ (1454, draft, withdrawn); /guides/ (1502, draft, withdrawn); /reactive-clay-slabs-as2870/ (1430, draft, withdrawn); /why-concrete-cracks/ (1215, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 15 | band_a_verdict_missing | 226 `concretejob2camden-226.jpg` | 15 refs / 14 pages; active 8 refs / 7 pages; withdrawn 7 refs / 7 pages. /commercial-concreting-gregory-hills/ (1474, draft, withdrawn); /concrete-driveway-replacement-narellan/ (1491, draft, withdrawn); /concrete-driveways-oran-park/ (1468, draft, withdrawn); /concrete-slabs-bringelly/ (1501, draft, withdrawn); /concrete-strength-grades-explained/ (1434, draft, withdrawn); /concreters-bargo/ (1424, draft, active); /concreters-cecil-park/ (1404, draft, active); /concreters-elizabeth-hills/ (1395, draft, active); /concreters-hoxton-park/ (1392, draft, active) x2; /concreters-mount-annan/ (1375, draft, active); /concreters-spring-farm/ (1377, draft, active); /exposed-aggregate-south-west-sydney/ (129, publish, active); /how-long-before-you-can-drive-on-concrete/ (1453, draft, withdrawn); /slab-thickness-for-driveways-vs-sheds/ (1436, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 16 | band_a_verdict_missing | 1185 `council-crossing-south-west-sydney-1185.jpg` | 15 refs / 14 pages; active 9 refs / 8 pages; withdrawn 6 refs / 6 pages. /commercial-hardstand-cost/ (1442, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-cobbitty/ (1498, draft, withdrawn); /concrete-paths-south-west-sydney/ (178, publish, active); /concrete-slabs-south-west-sydney/ (163, publish, active); /concreters-campbelltown/ (1405, draft, active) x2; /concreters-douglas-park/ (1421, draft, active); /concreters-grasmere/ (1382, draft, active); /concreters-leumeah/ (1406, draft, active); /concreters-oran-park/ (474, publish, active); /concreters-wilton/ (1417, draft, active); /driveway-crossover-cost-nsw/ (1428, draft, withdrawn); /salinity-and-concrete-western-sydney/ (1431, draft, withdrawn); /shed-and-garage-slabs-catherine-field/ (1486, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 17 | band_a_verdict_missing | 906 `driveway-excavation-camden-906.jpg` | 16 refs / 14 pages; active 9 refs / 7 pages; withdrawn 7 refs / 7 pages. /broom-finish-concrete/ (1447, draft, withdrawn); /commercial-concreting-narellan/ (1490, draft, withdrawn); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gregory-hills/ (1475, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gledswood-hills/ (1370, publish, active) x2; /concreters-kirkham/ (1381, draft, active); /concreters-narellan-vale/ (1373, draft, active) x2; /concreters-the-oaks/ (1423, draft, active); /control-joints-and-saw-cut-timing/ (1437, draft, withdrawn); /non-slip-finishes-for-pools-and-slopes/ (1448, draft, withdrawn); /what-actually-moves-a-concrete-quote/ (1443, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 18 | band_a_verdict_missing | 1150 `established-home-mount-annan-1150.jpg` | 15 refs / 14 pages; active 8 refs / 7 pages; withdrawn 7 refs / 7 pages. /coloured-concrete-explained/ (1445, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-catherine-field/ (1485, draft, withdrawn); /concrete-paths-edmondson-park/ (1487, draft, withdrawn); /concrete-slabs-south-west-sydney/ (163, publish, active); /concreters-camden-south/ (1380, draft, active); /concreters-currans-hill/ (1376, draft, active); /concreters-glenfield/ (1409, draft, active); /concreters-leppington/ (221, publish, active); /concreters-oran-park/ (474, publish, active); /concreters-west-hoxton/ (1391, draft, active) x2; /do-i-need-council-approval-driveway-nsw/ (1429, draft, withdrawn); /removing-oil-stains-and-tyre-marks-from-concrete/ (1456, draft, withdrawn); /wollondilly-council-driveway-crossing/ (1427, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 19 | band_a_verdict_missing | 1186 `gregory-hills-commercial-concreting-1186.webp` | 16 refs / 14 pages; active 10 refs / 8 pages; withdrawn 6 refs / 6 pages. /commercial-hardstand-cost/ (1442, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-cobbitty/ (1498, draft, withdrawn); /concrete-paths-south-west-sydney/ (178, publish, active); /concrete-slabs-south-west-sydney/ (163, publish, active); /concreters-campbelltown/ (1405, draft, active); /concreters-douglas-park/ (1421, draft, active) x2; /concreters-grasmere/ (1382, draft, active); /concreters-leumeah/ (1406, draft, active); /concreters-oran-park/ (474, publish, active); /concreters-wilton/ (1417, draft, active) x2; /driveway-crossover-cost-nsw/ (1428, draft, withdrawn); /salinity-and-concrete-western-sydney/ (1431, draft, withdrawn); /shed-and-garage-slabs-catherine-field/ (1486, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 20 | band_a_verdict_missing | 1187 `leppington-new-estates-1187.jpg` | 15 refs / 14 pages; active 9 refs / 8 pages; withdrawn 6 refs / 6 pages. /commercial-hardstand-cost/ (1442, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-cobbitty/ (1498, draft, withdrawn); /concrete-paths-south-west-sydney/ (178, publish, active); /concrete-slabs-south-west-sydney/ (163, publish, active); /concreters-carnes-hill/ (1393, draft, active); /concreters-douglas-park/ (1421, draft, active); /concreters-grasmere/ (1382, draft, active) x2; /concreters-leumeah/ (1406, draft, active); /concreters-oran-park/ (474, publish, active); /concreters-wilton/ (1417, draft, active); /driveway-crossover-cost-nsw/ (1428, draft, withdrawn); /salinity-and-concrete-western-sydney/ (1431, draft, withdrawn); /shed-and-garage-slabs-catherine-field/ (1486, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 21 | band_a_verdict_missing | 1152 `mount-annan-established-housing-1152.jpg` | 14 refs / 14 pages; active 7 refs / 7 pages; withdrawn 7 refs / 7 pages. /commercial-hardstand-cost/ (1442, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-catherine-field/ (1485, draft, withdrawn); /concrete-paths-edmondson-park/ (1487, draft, withdrawn); /concrete-slabs-south-west-sydney/ (163, publish, active); /concreters-campbelltown/ (1405, draft, active); /concreters-douglas-park/ (1421, draft, active); /concreters-glenfield/ (1409, draft, active); /concreters-leppington/ (221, publish, active); /concreters-oran-park/ (474, publish, active); /concreters-wilton/ (1417, draft, active); /driveway-crossover-cost-nsw/ (1428, draft, withdrawn); /salinity-and-concrete-western-sydney/ (1431, draft, withdrawn); /shed-and-garage-slabs-catherine-field/ (1486, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 22 | band_a_verdict_missing | 908 `oran-park-growth-estate-908.jpg` | 14 refs / 14 pages; active 7 refs / 7 pages; withdrawn 7 refs / 7 pages. /broom-finish-concrete/ (1447, draft, withdrawn); /commercial-concreting-narellan/ (1490, draft, withdrawn); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gregory-hills/ (1475, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gledswood-hills/ (1370, publish, active); /concreters-kirkham/ (1381, draft, active); /concreters-narellan/ (1372, draft, active); /concreters-the-oaks/ (1423, draft, active); /control-joints-and-saw-cut-timing/ (1437, draft, withdrawn); /non-slip-finishes-for-pools-and-slopes/ (1448, draft, withdrawn); /what-actually-moves-a-concrete-quote/ (1443, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 23 | band_a_verdict_missing | 480 `oran-park1-480.webp` | 16 refs / 14 pages; active 10 refs / 8 pages; withdrawn 6 refs / 6 pages. /commercial-concreting-narellan/ (1490, draft, withdrawn); /concrete-driveway-replacement-south-west-sydney/ (1366, publish, active); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gledswood-hills/ (1476, draft, withdrawn); /concrete-vs-pavers-vs-asphalt/ (1450, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gilead/ (1415, draft, active); /concreters-kemps-creek/ (1403, draft, active) x2; /concreters-mount-annan/ (1375, draft, active); /concreters-tahmoor/ (1419, draft, active) x2; /exposed-aggregate-vs-plain-concrete/ (1461, draft, withdrawn); /liverpool-council-vehicle-crossing/ (1425, draft, withdrawn); /stencilled-vs-stamped-concrete-cost/ (1440, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 24 | band_a_verdict_missing | 481 `oran-park2-481.webp` | 15 refs / 14 pages; active 9 refs / 8 pages; withdrawn 6 refs / 6 pages. /broom-finish-concrete/ (1447, draft, withdrawn); /commercial-concreting-narellan/ (1490, draft, withdrawn); /concrete-driveway-replacement-south-west-sydney/ (1366, publish, active); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gregory-hills/ (1475, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-cobbitty/ (1379, draft, active) x2; /concreters-gledswood-hills/ (1370, publish, active); /concreters-kemps-creek/ (1403, draft, active); /concreters-narellan-vale/ (1373, draft, active); /concreters-tahmoor/ (1419, draft, active); /control-joints-and-saw-cut-timing/ (1437, draft, withdrawn); /non-slip-finishes-for-pools-and-slopes/ (1448, draft, withdrawn); /what-actually-moves-a-concrete-quote/ (1443, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 25 | band_a_verdict_missing | 482 `oran-park3-482.webp` | 15 refs / 14 pages; active 8 refs / 7 pages; withdrawn 7 refs / 7 pages. /broom-finish-concrete/ (1447, draft, withdrawn); /commercial-concreting-narellan/ (1490, draft, withdrawn); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gregory-hills/ (1475, draft, withdrawn); /concreters-bringelly/ (1388, draft, active) x2; /concreters-cobbitty/ (1379, draft, active); /concreters-gledswood-hills/ (1370, publish, active); /concreters-kirkham/ (1381, draft, active); /concreters-narellan-vale/ (1373, draft, active); /concreters-the-oaks/ (1423, draft, active); /control-joints-and-saw-cut-timing/ (1437, draft, withdrawn); /non-slip-finishes-for-pools-and-slopes/ (1448, draft, withdrawn); /what-actually-moves-a-concrete-quote/ (1443, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 26 | band_a_verdict_missing | 956 `south-west-sydney-growth-corridor-956.png` | 15 refs / 15 pages; active 7 refs / 7 pages; withdrawn 8 refs / 8 pages. /campbelltown-council-driveway-crossing/ (1426, draft, withdrawn); /commercial-concreting-south-west-sydney/ (1369, publish, active); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-spring-farm/ (1493, draft, withdrawn); /concrete-slabs-leppington/ (1472, draft, withdrawn); /concreters-camden-park/ (1385, draft, active); /concreters-currans-hill/ (1376, draft, active); /concreters-gledswood-hills/ (1370, publish, active); /concreters-leppington/ (221, publish, active); /concreters-narellan/ (1372, draft, active); /concreters-wattle-grove/ (1402, draft, active); /curing-concrete-in-summer-vs-winter/ (1454, draft, withdrawn); /guides/ (1502, draft, withdrawn); /reactive-clay-slabs-as2870/ (1430, draft, withdrawn); /why-concrete-cracks/ (1215, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 27 | band_a_verdict_missing | 926 `stamped-concrete-south-west-sydney-926.jpg` | 17 refs / 15 pages; active 9 refs / 7 pages; withdrawn 8 refs / 8 pages. /campbelltown-council-driveway-crossing/ (1426, draft, withdrawn); /commercial-concreting-south-west-sydney/ (1369, publish, active); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-spring-farm/ (1493, draft, withdrawn); /concrete-slabs-leppington/ (1472, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-currans-hill/ (1376, draft, active); /concreters-gledswood-hills/ (1370, publish, active); /concreters-len-waters-estate/ (1396, draft, active) x2; /concreters-narellan/ (1372, draft, active); /concreters-theresa-park/ (1384, draft, active) x2; /curing-concrete-in-summer-vs-winter/ (1454, draft, withdrawn); /guides/ (1502, draft, withdrawn); /reactive-clay-slabs-as2870/ (1430, draft, withdrawn); /why-concrete-cracks/ (1215, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 28 | band_a_verdict_missing | 925 `stencil-concrete-south-west-sydney-925.webp` | 16 refs / 15 pages; active 8 refs / 7 pages; withdrawn 8 refs / 8 pages. /campbelltown-council-driveway-crossing/ (1426, draft, withdrawn); /commercial-concreting-south-west-sydney/ (1369, publish, active); /concrete-driveways-austral/ (1479, draft, withdrawn); /concrete-driveways-spring-farm/ (1493, draft, withdrawn); /concrete-slabs-gregory-hills/ (1475, draft, withdrawn); /concreters-bringelly/ (1388, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gledswood-hills/ (1370, publish, active); /concreters-len-waters-estate/ (1396, draft, active); /concreters-narellan/ (1372, draft, active) x2; /concreters-theresa-park/ (1384, draft, active); /curing-concrete-in-summer-vs-winter/ (1454, draft, withdrawn); /guides/ (1502, draft, withdrawn); /reactive-clay-slabs-as2870/ (1430, draft, withdrawn); /why-concrete-cracks/ (1215, draft, withdrawn) | HOLD only; still FAIL. Owner verdict required and none inferred. |
| 29 | false_geographic_remediation_pending | 1056 `south-creek-drainage-corridor-1056.jpg` | 16 refs / 15 pages; active 8 refs / 7 pages; withdrawn 8 refs / 8 pages. /campbelltown-council-driveway-crossing/ (1426, draft, withdrawn); /commercial-concreting-south-west-sydney/ (1369, publish, active); /concrete-driveways-catherine-field/ (1485, draft, withdrawn); /concrete-driveways-spring-farm/ (1493, draft, withdrawn); /concrete-slabs-leppington/ (1472, draft, withdrawn); /concreters-camden-park/ (1385, draft, active) x2; /concreters-currans-hill/ (1376, draft, active); /concreters-glen-alpine/ (1414, draft, active); /concreters-leppington/ (221, publish, active); /concreters-narellan/ (1372, draft, active); /concreters-wattle-grove/ (1402, draft, active); /curing-concrete-in-summer-vs-winter/ (1454, draft, withdrawn); /guides/ (1502, draft, withdrawn); /reactive-clay-slabs-as2870/ (1430, draft, withdrawn); /why-concrete-cracks/ (1215, draft, withdrawn) | D18/D20: Victorian Davis Creek cannot be named as South Creek. Applied: RENAME as aerial-waterway-residential-area-1056.jpg with alt 'Aerial view of a waterway beside a residential area' |
| 30 | false_geographic_remediation_pending | 1151 `reactive-clay-concreter-camden-1151.jpg` | 16 refs / 14 pages; active 9 refs / 7 pages; withdrawn 7 refs / 7 pages. /coloured-concrete-explained/ (1445, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-catherine-field/ (1485, draft, withdrawn); /concrete-paths-edmondson-park/ (1487, draft, withdrawn); /concrete-slabs-south-west-sydney/ (163, publish, active); /concreters-campbelltown/ (1405, draft, active); /concreters-currans-hill/ (1376, draft, active); /concreters-glenfield/ (1409, draft, active) x2; /concreters-leppington/ (221, publish, active); /concreters-oran-park/ (474, publish, active) x2; /concreters-west-hoxton/ (1391, draft, active); /do-i-need-council-approval-driveway-nsw/ (1429, draft, withdrawn); /removing-oil-stains-and-tyre-marks-from-concrete/ (1456, draft, withdrawn); /wollondilly-council-driveway-crossing/ (1427, draft, withdrawn) | D18/D20: remove unsupported geographic and geological assertion. Applied: RENAME as dry-cracked-ground-1151.jpg with alt 'Dry cracked ground surface' |
| 31 | false_geographic_remediation_pending | 1188 `reactive-clay-concreter-1-camden-1188.jpg` | 15 refs / 14 pages; active 8 refs / 7 pages; withdrawn 7 refs / 7 pages. /commercial-hardstand-cost/ (1442, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-cobbitty/ (1498, draft, withdrawn); /concrete-paths-south-west-sydney/ (178, publish, active); /concrete-slabs-south-west-sydney/ (163, publish, active); /concreters-carnes-hill/ (1393, draft, active); /concreters-eagle-vale/ (1412, draft, active); /concreters-grasmere/ (1382, draft, active); /concreters-leumeah/ (1406, draft, active) x2; /concreters-oran-park/ (474, publish, active); /decorative-concrete-harrington-park/ (1483, draft, withdrawn); /driveway-crossover-cost-nsw/ (1428, draft, withdrawn); /salinity-and-concrete-western-sydney/ (1431, draft, withdrawn); /shed-and-garage-slabs-catherine-field/ (1486, draft, withdrawn) | D18/D20: remove unsupported geographic and geological assertion. Applied: RENAME as dry-cracked-ground-1188.jpg with alt 'Dry cracked ground surface' |
| 32 | band_b_derivative_disposition_missing | 46 `concrete-tesimonial-4-camden-46.webp` | 17 refs / 15 pages; active 8 refs / 6 pages; withdrawn 9 refs / 9 pages. /concrete-driveway-replacement-mount-annan/ (1492, draft, withdrawn); /concrete-driveways-edmondson-park/ (1489, draft, withdrawn); /concrete-efflorescence/ (1455, draft, withdrawn); /concrete-patios-gledswood-hills/ (1478, draft, withdrawn); /concrete-vs-pavers/ (1459, draft, withdrawn); /concreters-catherine-field/ (1371, draft, active) x2; /concreters-edmondson-park/ (1387, draft, active); /concreters-gregory-hills/ (969, publish, active); /concreters-menangle/ (1422, draft, active); /concreters-prestons/ (1398, draft, active); /diy-concrete-vs-hiring-a-concreter/ (1462, draft, withdrawn); /exposed-aggregate-cost/ (1439, draft, withdrawn); /homepage/ (12, publish, active) x2; /shed-and-garage-slabs-oran-park/ (1469, draft, withdrawn); /shed-slab-cost/ (1441, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: RENAME as exposed-aggregate-front-paths-46.webp with alt "Exposed aggregate paths leading to a home's front entry" |
| 33 | band_b_derivative_disposition_missing | 52 `concrete-testimonial-1-1-camden-52.webp` | 16 refs / 15 pages; active 8 refs / 7 pages; withdrawn 8 refs / 8 pages. /commercial-concreting-bringelly/ (1500, draft, withdrawn); /concrete-driveway-replacement-mount-annan/ (1492, draft, withdrawn); /concrete-driveways-edmondson-park/ (1489, draft, withdrawn); /concrete-repair-vs-replace/ (1452, draft, withdrawn); /concrete-slabs-austral/ (1480, draft, withdrawn); /concreters-appin/ (1420, draft, active) x2; /concreters-catherine-field/ (1371, draft, active); /concreters-elderslie/ (1378, draft, active); /concreters-harrington-park/ (1126, publish, active); /concreters-middleton-grange/ (1390, draft, active); /concreters-rossmore/ (1389, draft, active); /exposed-aggregate-gledswood-hills/ (1477, draft, withdrawn); /exposed-aggregate-vs-stencil/ (1444, draft, withdrawn); /shed-and-garage-slabs-south-west-sydney/ (1367, publish, active); /site-classification-explained/ (1433, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: RENAME as fresh-concrete-pool-surround-52.webp with alt 'Freshly poured concrete beside a swimming pool' |
| 34 | band_b_derivative_disposition_missing | 49 `concrete-testimonial-1-camden-49.webp` | 16 refs / 15 pages; active 9 refs / 8 pages; withdrawn 7 refs / 7 pages. /commercial-concreting-bringelly/ (1500, draft, withdrawn); /concrete-driveway-replacement-mount-annan/ (1492, draft, withdrawn); /concrete-driveways-edmondson-park/ (1489, draft, withdrawn); /concrete-efflorescence/ (1455, draft, withdrawn); /concrete-patios-south-west-sydney/ (195, publish, active); /concreters-appin/ (1420, draft, active); /concreters-catherine-field/ (1371, draft, active); /concreters-edmondson-park/ (1387, draft, active); /concreters-harrington-park/ (1126, publish, active); /concreters-menangle/ (1422, draft, active) x2; /concreters-raby/ (1411, draft, active); /diy-concrete-vs-hiring-a-concreter/ (1462, draft, withdrawn); /exposed-aggregate-cost/ (1439, draft, withdrawn); /shed-and-garage-slabs-south-west-sydney/ (1367, publish, active); /shed-slab-cost/ (1441, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: RENAME as fresh-concrete-pool-surround-49.webp with alt 'Freshly poured concrete beside a swimming pool' |
| 35 | band_b_derivative_disposition_missing | 51 `concrete-testimonial-2-camden-51.webp` | 15 refs / 15 pages; active 7 refs / 7 pages; withdrawn 8 refs / 8 pages. /commercial-concreting-bringelly/ (1500, draft, withdrawn); /concrete-driveway-replacement-mount-annan/ (1492, draft, withdrawn); /concrete-driveways-edmondson-park/ (1489, draft, withdrawn); /concrete-repair-vs-replace/ (1452, draft, withdrawn); /concrete-slabs-austral/ (1480, draft, withdrawn); /concreters-appin/ (1420, draft, active); /concreters-catherine-field/ (1371, draft, active); /concreters-elderslie/ (1378, draft, active); /concreters-harrington-park/ (1126, publish, active); /concreters-middleton-grange/ (1390, draft, active); /concreters-raby/ (1411, draft, active); /exposed-aggregate-gledswood-hills/ (1477, draft, withdrawn); /exposed-aggregate-vs-stencil/ (1444, draft, withdrawn); /shed-and-garage-slabs-south-west-sydney/ (1367, publish, active); /site-classification-explained/ (1433, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: RENAME as concrete-stepping-slabs-garden-path-51.webp with alt 'Concrete stepping slabs laid through a garden' |
| 36 | band_b_derivative_disposition_missing | 48 `concrete-testimonial-3-camden-48.webp` | 15 refs / 15 pages; active 8 refs / 8 pages; withdrawn 7 refs / 7 pages. /concrete-driveway-replacement-mount-annan/ (1492, draft, withdrawn); /concrete-driveways-edmondson-park/ (1489, draft, withdrawn); /concrete-efflorescence/ (1455, draft, withdrawn); /concrete-patios-south-west-sydney/ (195, publish, active); /concrete-vs-pavers/ (1459, draft, withdrawn); /concreters-catherine-field/ (1371, draft, active); /concreters-edmondson-park/ (1387, draft, active); /concreters-harrington-park/ (1126, publish, active); /concreters-menangle/ (1422, draft, active); /concreters-raby/ (1411, draft, active); /diy-concrete-vs-hiring-a-concreter/ (1462, draft, withdrawn); /exposed-aggregate-cost/ (1439, draft, withdrawn); /homepage/ (12, publish, active); /shed-and-garage-slabs-south-west-sydney/ (1367, publish, active); /shed-slab-cost/ (1441, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: RENAME as exposed-aggregate-residential-driveway-48.webp with alt 'Exposed aggregate driveway leading to a carport' |
| 37 | band_b_derivative_disposition_missing | 47 `concrete-testimonial-6-camden-47.webp` | 15 refs / 15 pages; active 8 refs / 8 pages; withdrawn 7 refs / 7 pages. /concrete-driveway-replacement-mount-annan/ (1492, draft, withdrawn); /concrete-driveways-edmondson-park/ (1489, draft, withdrawn); /concrete-efflorescence/ (1455, draft, withdrawn); /concrete-patios-south-west-sydney/ (195, publish, active); /concrete-vs-pavers/ (1459, draft, withdrawn); /concreters-catherine-field/ (1371, draft, active); /concreters-edmondson-park/ (1387, draft, active); /concreters-harrington-park/ (1126, publish, active); /concreters-menangle/ (1422, draft, active); /concreters-raby/ (1411, draft, active); /diy-concrete-vs-hiring-a-concreter/ (1462, draft, withdrawn); /exposed-aggregate-cost/ (1439, draft, withdrawn); /homepage/ (12, publish, active); /shed-and-garage-slabs-south-west-sydney/ (1367, publish, active); /shed-slab-cost/ (1441, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: RENAME as fresh-concrete-backyard-slab-47.webp with alt 'Freshly poured concrete slab beside a two-storey home' |
| 38 | band_b_derivative_disposition_missing | 228 `concretejob1camden-228.jpg` | 16 refs / 14 pages; active 10 refs / 8 pages; withdrawn 6 refs / 6 pages. /commercial-concreting-gregory-hills/ (1474, draft, withdrawn); /concrete-driveway-replacement-south-west-sydney/ (1366, publish, active); /concrete-driveways-oran-park/ (1468, draft, withdrawn); /concrete-slabs-gledswood-hills/ (1476, draft, withdrawn); /concrete-strength-grades-explained/ (1434, draft, withdrawn); /concreters-bargo/ (1424, draft, active) x2; /concreters-cecil-park/ (1404, draft, active); /concreters-ellis-lane/ (1383, draft, active); /concreters-ingleburn/ (1408, draft, active); /concreters-mount-annan/ (1375, draft, active) x2; /concreters-spring-farm/ (1377, draft, active); /exposed-aggregate-south-west-sydney/ (129, publish, active); /how-long-before-you-can-drive-on-concrete/ (1453, draft, withdrawn); /slab-thickness-for-driveways-vs-sheds/ (1436, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: RENAME as fresh-concrete-side-yard-slab-228.jpg with alt 'Freshly poured concrete slab along a side boundary' |
| 39 | band_b_derivative_disposition_missing | 280 `image-testemonials-camden-280.jpeg` | 14 refs / 14 pages; active 8 refs / 8 pages; withdrawn 6 refs / 6 pages. /commercial-concreting-gregory-hills/ (1474, draft, withdrawn); /concrete-driveway-replacement-south-west-sydney/ (1366, publish, active); /concrete-driveways-south-west-sydney/ (105, publish, active); /concrete-slabs-gledswood-hills/ (1476, draft, withdrawn); /concrete-vs-pavers-vs-asphalt/ (1450, draft, withdrawn); /concreters-bradbury/ (1413, draft, active); /concreters-cobbitty/ (1379, draft, active); /concreters-gilead/ (1415, draft, active); /concreters-kemps-creek/ (1403, draft, active); /concreters-mount-annan/ (1375, draft, active); /concreters-tahmoor/ (1419, draft, active); /exposed-aggregate-vs-plain-concrete/ (1461, draft, withdrawn); /liverpool-council-vehicle-crossing/ (1425, draft, withdrawn); /stencilled-vs-stamped-concrete-cost/ (1440, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: EXCLUDE |
| 40 | band_b_derivative_disposition_missing | 1067 `verified-badge-e1784545689665-camden-1067.avif` | 14 refs / 14 pages; active 6 refs / 6 pages; withdrawn 8 refs / 8 pages. /coloured-concrete-explained/ (1445, draft, withdrawn); /concrete-driveway-replacement-currans-hill/ (1497, draft, withdrawn); /concrete-driveways-catherine-field/ (1485, draft, withdrawn); /concrete-driveways-spring-farm/ (1493, draft, withdrawn); /concrete-slabs-leppington/ (1472, draft, withdrawn); /concreters-camden-south/ (1380, draft, active); /concreters-currans-hill/ (1376, draft, active); /concreters-glen-alpine/ (1414, draft, active); /concreters-leppington/ (221, publish, active); /concreters-narellan/ (1372, draft, active); /concreters-west-hoxton/ (1391, draft, active); /do-i-need-council-approval-driveway-nsw/ (1429, draft, withdrawn); /removing-oil-stains-and-tyre-marks-from-concrete/ (1456, draft, withdrawn); /wollondilly-council-driveway-crossing/ (1427, draft, withdrawn) | owner-recorded Band B verdict; build/45-media-remediation.csv. Applied: EXCLUDE |

**Reconciliation: 12 denied + 16 Band A + 3 false-geography + 9 Band B = 40.**
Thirty-four now pass; the 16 Band A assertions remain failed by design.

## Band A verdict table

All 16 owner verdict cells are blank. No OK, GENERIC, REPLACE or UNUSABLE decision was inferred.

| Tile | ID | Held filename | Claim recorded by worksheet | Verdict | Payload state |
|---:|---:|---|---|---|---|
| 1 | 907 | `camden-town-centre-907.jpg` | Filename and alt assert this is Camden town centre. | **BLANK** | HOLD; public false, derivative false |
| 2 | 924 | `coloured-concrete-south-west-sydney-924.png` | Filename and alt assert South West Sydney. | **BLANK** | HOLD; public false, derivative false |
| 3 | 226 | `concretejob2camden-226.jpg` | Filename asserts the job is in Camden. | **BLANK** | HOLD; public false, derivative false |
| 4 | 1185 | `council-crossing-south-west-sydney-1185.jpg` | Filename and alt assert a council crossing in South West Sydney. | **BLANK** | HOLD; public false, derivative false |
| 5 | 906 | `driveway-excavation-camden-906.jpg` | Filename and alt assert the excavation is in Camden. | **BLANK** | HOLD; public false, derivative false |
| 6 | 1150 | `established-home-mount-annan-1150.jpg` | Filename and alt assert an established home in Mount Annan, NSW. | **BLANK** | HOLD; public false, derivative false |
| 7 | 1186 | `gregory-hills-commercial-concreting-1186.webp` | Filename and alt assert commercial concreting in Gregory Hills, NSW. | **BLANK** | HOLD; public false, derivative false |
| 8 | 1187 | `leppington-new-estates-1187.jpg` | Filename and alt assert new estates in Leppington, NSW. | **BLANK** | HOLD; public false, derivative false |
| 9 | 1152 | `mount-annan-established-housing-1152.jpg` | Filename and alt assert established housing in Mount Annan, NSW. | **BLANK** | HOLD; public false, derivative false |
| 10 | 908 | `oran-park-growth-estate-908.jpg` | Filename and alt assert an Oran Park growth estate. | **BLANK** | HOLD; public false, derivative false |
| 11 | 480 | `oran-park1-480.webp` | Filename asserts Oran Park, NSW. | **BLANK** | HOLD; public false, derivative false |
| 12 | 481 | `oran-park2-481.webp` | Filename asserts Oran Park, NSW. | **BLANK** | HOLD; public false, derivative false |
| 13 | 482 | `oran-park3-482.webp` | Filename asserts Oran Park, NSW. | **BLANK** | HOLD; public false, derivative false |
| 14 | 956 | `south-west-sydney-growth-corridor-956.png` | Filename and alt assert the South West Sydney growth corridor. | **BLANK** | HOLD; public false, derivative false |
| 15 | 926 | `stamped-concrete-south-west-sydney-926.jpg` | Filename and alt assert South West Sydney. | **BLANK** | HOLD; public false, derivative false |
| 16 | 925 | `stencil-concrete-south-west-sydney-925.webp` | Filename and alt assert South West Sydney. | **BLANK** | HOLD; public false, derivative false |

All 16 are present in `source-inputs/media-held-band-a/`. This is an unresolved
placement state, not a substantive media verdict.

## Band B transformation table

| ID | Verdict | Source refs (active / withdrawn) | Final filename | Alt or slot action | Result |
|---:|---|---:|---|---|---|
| 46 | GENERIC | 17 (8 / 9) | `exposed-aggregate-front-paths-46.webp` | Exposed aggregate paths leading to a home's front entry | **PASS** |
| 52 | GENERIC | 16 (8 / 8) | `fresh-concrete-pool-surround-52.webp` | Freshly poured concrete beside a swimming pool | **PASS** |
| 49 | GENERIC | 16 (9 / 7) | `fresh-concrete-pool-surround-49.webp` | Freshly poured concrete beside a swimming pool | **PASS** |
| 51 | GENERIC | 15 (7 / 8) | `concrete-stepping-slabs-garden-path-51.webp` | Concrete stepping slabs laid through a garden | **PASS** |
| 48 | GENERIC | 15 (8 / 7) | `exposed-aggregate-residential-driveway-48.webp` | Exposed aggregate driveway leading to a carport | **PASS** |
| 47 | GENERIC | 15 (8 / 7) | `fresh-concrete-backyard-slab-47.webp` | Freshly poured concrete slab beside a two-storey home | **PASS** |
| 228 | GENERIC | 16 (10 / 6) | `fresh-concrete-side-yard-slab-228.jpg` | Freshly poured concrete slab along a side boundary | **PASS** |
| 280 | UNUSABLE | 14 (8 / 6) | EXCLUDED | record and every slot absent; no replacement | **PASS** |
| 1067 | UNUSABLE | 14 (6 / 8) | EXCLUDED | record and every slot absent; no replacement | **PASS** |

The 28 UNUSABLE slots reconcile exactly:

```text
  attachment 280   source 14 = active  8 + withdrawn  6
  attachment 1067  source 14 = active  6 + withdrawn  8
  total            source 28 = active 14 + withdrawn 14
```

Two active slots disappeared inside D32 sections and 12 were directly pruned; the 14 withdrawn
slots disappeared with their pages. Zero stale URL, filename, metadata or Elementor reference
survives for either asset.

The four Band B local-project cards removed with D32 were: 46 on Gregory Hills; 48 and 49 on
Edmondson Park; and 52 on Catherine Field. They remain non-evidential and were not restocked.

Pair 49/52 remains two IDs and filenames despite identical bytes. E&T pair 468/471 was excluded
together. No attachment identity was collapsed.

## Renamed public assets

There are no plain RETAIN rows. D24/D20 required reversal of the Stage 8 geographic naming
convention, so all 51 permitted public files are RENAME rows.

| ID | Band | Payload source filename | Public filename | Public alt |
|---:|---|---|---|---|
| 17 | D | `concrete-project-detail-camden-17.jpg` | `concrete-project-detail-17.jpg` | Concrete project detail |
| 18 | D | `concrete-project-detail-camden-18.jpg` | `concrete-project-detail-18.jpg` | Concrete project detail |
| 19 | D | `concrete-project-detail-camden-19.jpg` | `concrete-project-detail-19.jpg` | Concrete project detail |
| 46 | B | `concrete-tesimonial-4-camden-46.webp` | `exposed-aggregate-front-paths-46.webp` | Exposed aggregate paths leading to a home's front entry |
| 47 | B | `concrete-testimonial-6-camden-47.webp` | `fresh-concrete-backyard-slab-47.webp` | Freshly poured concrete slab beside a two-storey home |
| 48 | B | `concrete-testimonial-3-camden-48.webp` | `exposed-aggregate-residential-driveway-48.webp` | Exposed aggregate driveway leading to a carport |
| 49 | B | `concrete-testimonial-1-camden-49.webp` | `fresh-concrete-pool-surround-49.webp` | Freshly poured concrete beside a swimming pool |
| 50 | D | `exposed-aggregate-concrete-camden-50.jpg` | `exposed-aggregate-concrete-50.jpg` | Exposed aggregate concrete |
| 51 | B | `concrete-testimonial-2-camden-51.webp` | `concrete-stepping-slabs-garden-path-51.webp` | Concrete stepping slabs laid through a garden |
| 52 | B | `concrete-testimonial-1-1-camden-52.webp` | `fresh-concrete-pool-surround-52.webp` | Freshly poured concrete beside a swimming pool |
| 53 | D | `patiosandpathways-camden-53.webp` | `patiosandpathways-53.webp` | Patiosandpathways |
| 54 | D | `coloured-detailed-concrete-camden-54.jpg` | `coloured-detailed-concrete-54.jpg` | Coloured detailed concrete |
| 55 | D | `patiosconcrete-camden-55.jpg` | `patiosconcrete-55.jpg` | Patiosconcrete |
| 121 | D | `reinforcedheavydutyconcrete-camden-121.webp` | `reinforcedheavydutyconcrete-121.webp` | Reinforcedheavydutyconcrete |
| 144 | D | `paths-and-pathwaysconcrete-camden-144.jpg` | `paths-and-pathwaysconcrete-144.jpg` | Paths and pathwaysconcrete |
| 145 | D | `patiosandalfrescoconcrete-camden-145.jpg` | `patiosandalfrescoconcrete-145.jpg` | Patiosandalfrescoconcrete |
| 146 | D | `concretepoolsurronds-camden-146.jpg` | `concretepoolsurronds-146.jpg` | Concretepoolsurronds |
| 166 | D | `shedslabconcrete-camden-166.jpg` | `shedslabconcrete-166.jpg` | Shedslabconcrete |
| 167 | D | `garage-slabs-concrete-camden-167.jpg` | `garage-slabs-concrete-167.jpg` | Garage slabs concrete |
| 168 | D | `extension-and-floor-slabs-concrete-camden-168.jpg` | `extension-and-floor-slabs-concrete-168.jpg` | Extension and floor slabs concrete |
| 181 | D | `side-access-paths-concrete-camden-181.jpg` | `side-access-paths-concrete-181.jpg` | Side access paths concrete |
| 182 | D | `concrete-garden-paths-and-connecting-paths-concrete-camden-182.jpg` | `concrete-garden-paths-and-connecting-paths-concrete-182.jpg` | Concrete garden paths and connecting paths concrete |
| 183 | D | `front-and-entry-paths-concrete-camden-183.jpg` | `front-and-entry-paths-concrete-183.jpg` | Front and entry paths concrete |
| 184 | D | `accessible-paths-concrete-camden-184.jpg` | `accessible-paths-concrete-184.jpg` | Accessible paths concrete |
| 227 | D | `backyard-patio-concreter-camden-227.jpg` | `backyard-patio-concreter-227.jpg` | Backyard patio concreter |
| 228 | B | `concretejob1camden-228.jpg` | `fresh-concrete-side-yard-slab-228.jpg` | Freshly poured concrete slab along a side boundary |
| 275 | D | `image-placeholder-hero-camden-275.jpeg` | `image-placeholder-hero-275.jpeg` | (empty decorative alt) |
| 276 | D | `image-contact-1-camden-276.jpg` | `image-contact-1-276.jpg` | (empty decorative alt) |
| 277 | D | `image-placeholder-hero-1-camden-277.jpeg` | `image-placeholder-hero-1-277.jpeg` | (empty decorative alt) |
| 278 | D | `image-placeholder-about-1-camden-278.jpeg` | `image-placeholder-about-1-278.jpeg` | (empty decorative alt) |
| 279 | D | `image-placeholder-about-camden-279.jpeg` | `image-placeholder-about-279.jpeg` | (empty decorative alt) |
| 323 | D | `about-2-hero-camden-323.jpg` | `about-2-hero-323.jpg` | (empty decorative alt) |
| 609 | D | `exposed-aggregate-south-west-sydney-609.jpg` | `exposed-aggregate-residential-driveway-609.jpg` | Exposed aggregate driveway leading to a home |
| 909 | D | `control-joints-and-cracks-camden-909.jpg` | `control-joints-and-cracks-909.jpg` | Control joints and cracks |
| 927 | D | `honed-and-polished-concrete-camden-927.webp` | `honed-and-polished-concrete-927.webp` | Honed and polished concrete |
| 1056 | D | `south-creek-drainage-corridor-1056.jpg` | `aerial-waterway-residential-area-1056.jpg` | Aerial view of a waterway beside a residential area |
| 1065 | D | `concrete-slabs-camden-1065.jpg` | `concrete-slabs-1065.jpg` | Concrete slabs |
| 1066 | D | `pouring-a-concrete-slab-camden-1066.jpg` | `pouring-a-concrete-slab-1066.jpg` | Pouring a concrete slab |
| 1068 | D | `what-is-a-concrete-slab-camden-1068.jpg` | `what-is-a-concrete-slab-1068.jpg` | What is a concrete slab |
| 1109 | D | `what-is-exposed-aggregate-camden-1109.jpg` | `what-is-exposed-aggregate-1109.jpg` | What is exposed aggregate |
| 1151 | D | `reactive-clay-concreter-camden-1151.jpg` | `dry-cracked-ground-1151.jpg` | Dry cracked ground surface |
| 1153 | D | `camden-council-driveway-crossing-1153.jpg` | `concrete-vehicle-crossing-1153.jpg` | Concrete vehicle crossing between a kerb and property boundary |
| 1188 | D | `reactive-clay-concreter-1-camden-1188.jpg` | `dry-cracked-ground-1188.jpg` | Dry cracked ground surface |
| 1230 | D | `shrinkage-cracks-camden-1230.jpg` | `shrinkage-cracks-1230.jpg` | Shrinkage cracks |
| 1231 | D | `settlement-cracks-camden-1231.jpg` | `settlement-cracks-1231.jpg` | Settlement cracks |
| 1232 | D | `heave-cracks-camden-1232.jpg` | `heave-cracks-1232.jpg` | Heave cracks |
| 1233 | D | `structural-cracks-camden-1233.jpg` | `structural-cracks-1233.jpg` | Structural cracks |
| 1345 | D | `concrete-sealing-camden-1345.jpg` | `concrete-sealing-1345.jpg` | Concrete sealing |
| 1359 | D | `concrete-driveway-cracks-camden-1359.jpg` | `concrete-driveway-cracks-1359.jpg` | Concrete driveway cracks |
| 1361 | D | `concrete-driveway-cracks-1-camden-1361.jpg` | `concrete-driveway-cracks-1-1361.jpg` | Concrete driveway cracks 1 |
| 1362 | D | `concrete-driveway-cracks-2-camden-1362.jpg` | `concrete-driveway-cracks-2-1362.jpg` | Concrete driveway cracks 2 |

## Excluded assets

| ID | Band | Filename | Authority |
|---:|---|---|---|
| 159 | D | `chatgpt-image-jul-6-2026-01-52-19-pm-camden-159.png` | D24/D36 retired AI/source-brand attachment |
| 177 | D | `cropped-chatgpt-image-jul-6-2026-07-59-41-pm-camden-177.png` | D24/D36 retired AI/source-brand attachment |
| 250 | D | `corex-concreters-camden-logo-250.png` | Astra product mark, not a Structure Co asset |
| 272 | D | `cropped-chatgpt-image-jul-6-2026-01-52-19-pm-camden-272.png` | D24 and C2PA/AI provenance finding |
| 280 | B | `image-testemonials-camden-280.jpeg` | owner-recorded Band B verdict; build/45-media-remediation.csv |
| 306 | C | `corex-concreters-camden-logo-306.png` | D18/D36 retired E&T brand attachment |
| 307 | C | `corex-concreters-camden-logo-307.png` | D18/D36 retired E&T brand attachment |
| 308 | D | `corex-concreters-camden-logo-308.png` | D24 and C2PA/AI provenance finding |
| 309 | D | `corex-concreters-camden-logo-309.png` | D24 and C2PA/AI provenance finding |
| 422 | C | `corex-concreters-camden-logo-422.png` | D18/D36 retired E&T brand attachment |
| 468 | D | `corex-concreters-camden-logo-468.png` | E&T Concreters Melbourne wordmark; duplicate contract requires pair treatment |
| 469 | C | `corex-concreters-camden-logo-469.png` | D18/D36 retired E&T brand attachment |
| 471 | D | `corex-concreters-camden-logo-471.png` | E&T Concreters Melbourne wordmark; duplicate contract requires pair treatment |
| 472 | C | `corex-concreters-camden-logo-472.png` | D18/D36 retired E&T brand attachment |
| 1020 | D | `wianamatta-shale-clay-camden-1020.jpg` | D19 removes the Tarneit soil photograph and retains its containing sections |
| 1067 | B | `verified-badge-e1784545689665-camden-1067.avif` | owner-recorded Band B verdict; build/45-media-remediation.csv |

The exclusions cover the seven recorded retired E&T IDs; unauthorised AI; D19 soil 1020;
Band B 280/1067; Astra mark 250; and E&T pair 468/471. All remain recoverable in
`source-inputs/media-retired/`.

The old in-page E&T slots are clear. Structure Co brand assets were not imported. The future
database verifier now requires `structure-co-horizontal.svg` in the header and
`structure-co-icon-512.png` as the site icon. Assignment remains an unexecuted staging task.

## D32 section removal

| Page ID | Slug | Sections removed | Markers removed |
|---:|---|---:|---:|
| 221 | `/concreters-leppington/` | 1 | 3 |
| 474 | `/concreters-oran-park/` | 1 | 3 |
| 969 | `/concreters-gregory-hills/` | 1 | 3 |
| 1126 | `/concreters-harrington-park/` | 1 | 3 |
| 1163 | `/concreters-austral/` | 1 | 3 |
| 1365 | `/gallery/` | 2 | 2 |
| 1370 | `/concreters-gledswood-hills/` | 1 | 3 |
| 1371 | `/concreters-catherine-field/` | 1 | 3 |
| 1372 | `/concreters-narellan/` | 1 | 3 |
| 1375 | `/concreters-mount-annan/` | 1 | 3 |
| 1376 | `/concreters-currans-hill/` | 1 | 3 |
| 1377 | `/concreters-spring-farm/` | 1 | 3 |
| 1378 | `/concreters-elderslie/` | 1 | 3 |
| 1379 | `/concreters-cobbitty/` | 1 | 3 |
| 1387 | `/concreters-edmondson-park/` | 1 | 3 |
| 1388 | `/concreters-bringelly/` | 1 | 3 |

Total: **17 sections on 16 pages; 47 markers**. The old
15-versus-16 mismatch was gallery: 15 suburb modules use local-work-card, while gallery has
two differently structured evidential sections.

## Six delivery collision-renames

No filename containing space-parenthesis-1 remains in public, held or retired directories.

| ID | Final location | Treatment |
|---:|---|---|
| 226 | `media-held-band-a/concretejob2camden-226.jpg` | Band A HOLD |
| 227 | `media/backyard-patio-concreter-227.jpg` | public D24 generic |
| 228 | `media/fresh-concrete-side-yard-slab-228.jpg` | public Band B GENERIC |
| 468 | `media-retired/corex-concreters-camden-logo-468.png` | E&T pair excluded |
| 471 | `media-retired/corex-concreters-camden-logo-471.png` | E&T pair excluded |
| 609 | `media/exposed-aggregate-residential-driveway-609.jpg` | Adelaide/SWS naming removed |

## Controls implemented

- Complete 83-row manifest generation with 16 blank-verdict Band A HOLD rows.
- Reproducible WXR transformation: D32, filename/title/alt updates, metadata length repair,
  excluded/held record and slot removal, wp_css exclusion and media-reference resolution.
- Public-directory parity and recoverable held/retired quarantines.
- Public media gate that compares binaries and derivative and fails only the 16 missing verdicts.
- Full manifest consumption by the media audit, re-encode driver and local media importer.
- Retired post-import Band B mutator, which now refuses execution.
- Post-import assertions for denied/held media, D32, wp_css and supplied brand assignments.

## Changed-file list

Git tracks zero files, so diff cannot infer a baseline. Exact pass-owned implementation paths:

```text
  lib/media_payload.py
  scripts/22-media-audit.py
  scripts/22-reencode-images.sh
  scripts/28-preflight.sh
  scripts/37-preconditions.py
  scripts/45-band-b-verify.py
  scripts/46-architecture-import-gate.py
  scripts/46-claim-evidence-gate.py
  scripts/46-public-media-gate.py
  scripts/46-source-brand-gate.py
  scripts/47-apply-media-files.py
  scripts/47-media-blocker-inventory.py
  scripts/47-write-report.py
  tests/test_preimport_safety.py
  tests/test_phase_b_media_payload.py
  staging-authoritative/scripts/import-media-local.sh
  staging-authoritative/scripts/apply-band-b-remediation.php
  staging-authoritative/scripts/apply-band-b-remediation.sh
  staging-authoritative/scripts/verify-post-import.php
  reports/post-import-tasks.md
  CONTEXT.md
  build/46-active-main-import.xml
  build/46-active-page-allowlist.json
  build/46-public-media-policy.json
  build/46-claim-register.json
  build/47-media-remediation.csv
  reports/47-original-media-blockers.json
  reports/47-media-file-application.json
  reports/47-phase-b-media-payload-closure.md
  regenerated reports/22, reports/28 and reports/46 gate evidence
  source-inputs/media (51 public files)
  source-inputs/media-retired (16 exclusions)
  source-inputs/media-held-band-a (16 holds)
```

## Verification results

| Command | Result |
|---|---|
| `python scripts/21-encoding-canary.py` | PASS — all three exact assertions |
| `python scripts/46-architecture-import-gate.py --check` | PASS — reproducible |
| `python scripts/47-apply-media-files.py --check` | PASS — public 51 |
| `python scripts/22-media-audit.py` | PASS — 51/51 |
| `python scripts/22-astra-audit.py` | PASS |
| `python scripts/46-source-brand-gate.py` | PASS — reader-visible CoreX 0 |
| `python scripts/46-claim-evidence-gate.py` | expected FAIL — 144/140 unsupported |
| `python scripts/46-public-media-gate.py` | expected FAIL — 16 Band A only; Band B 0 |
| `python scripts/37-preconditions.py` | expected BLOCKED — all phases |
| `scripts/28-preflight.sh` | NO-GO — Gates 7, 12, 16, 17 |
| `python -m pytest -q` | PASS — 18 tests |
| shell syntax checks | PASS |
| PHP CLI syntax/runtime check | unavailable locally and in WSL; verifier remains unexecuted until authorised staging |
| `git diff --check` | PASS; limitation: zero tracked files |

### Immutable hashes

| File | Expected | Computed | Result |
|---|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | MATCH |

### Phase table

| Phase | Name | Status | Evidence |
|---|---|---|---|
| A | figures | BLOCKED | 91 false, 0 true |
| B | media/staging | BLOCKED | public 51/51; excluded 16/16; held 16/16; 16 verdicts missing |
| C | identity/schema | BLOCKED | 1 true, 19 false |
| D | Liverpool | BLOCKED | council specs absent |
| E | service rebuild | BLOCKED | requires A |
| F | images | BLOCKED | requires A–E |
| G | release | BLOCKED | requires prior phases and GO |

### Preflight

| Gate | Result | Detail |
|---:|---|---|
| 1 | PASS | UTF-8 |
| 2 | PASS | Stage 9 15/15 |
| 3 | PASS | ID collisions |
| 4 | PASS | media 51/51 |
| 5 | PASS | Astra |
| 6 | PASS | immutable image references |
| 7 | **FAIL** | uniqueness: 1,761 5-grams; 1,491 pairs |
| 8 | PASS | intersections |
| 9 | PASS | menu lint |
| 10 | PASS | Victorian blocklist |
| 11 | PASS | schema placeholders |
| 12 | **FAIL** | coherence: 90 SEVERE, 139 over threshold, 0.8244 filler |
| 13 | PASS | source brand |
| 14 | PASS | assigned menus |
| 15 | PASS | active/import parity |
| 16 | **FAIL** | claims 144; unsupported 140 |
| 17 | **FAIL** | Band A blank 16; Band B fail 0 |
| **Overall** | **NO-GO** | any fail is build-failing |

## Remaining Phase B work

1. **Owner:** record an unambiguous verdict and required note for each of the 16 Band A tiles.
2. **Agent after input:** encode authorised generic/replacement/removal actions, regenerate, and
   rerun the same gates without weakening them.
3. **Owner:** explicitly authorise any staging import.
4. **Agent during authorised staging:** import only allowlisted artifacts, assign the supplied
   Structure Co header/favicon and execute the database/rendered verifier.

The 45 unresearched suburbs remain deferred under D22. Identity, service specifications,
Liverpool evidence, unsupported claims, coherence and uniqueness remain separate blockers.

## No-action confirmation

**No WordPress import, remote fetch, deployment, publication, indexability change or immutable/
governing-file edit occurred.** No unsupported business claim was rewritten. The only
claim-bearing removal was the already-authorised D32 evidential-module removal.
