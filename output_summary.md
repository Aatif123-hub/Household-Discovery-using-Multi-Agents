# Summary

### Summary of Entity Resolution

#### Direct Matching

| Record ID | Name                      | Address                           | City                | State | ZIP     | SSN         | Phone Number  | Explanation                                                                 |
|------------|---------------------------|-----------------------------------|---------------------|-------|---------|-------------|---------------|-----------------------------------------------------------------------------|
| A908334    | ANTHONY A MATRENS         | 521 COCHRAN AVEN                  | SAN DIEGTO          | CA    | 92154   | 202100234   | NaN           | Direct match with A931754 by name and address with minor variations.      |
| A931754    | TONY A MARTENS            | 521 Cochran Avn                   | San Diego           | Ca    | 92154   | 22100234    | NaN           | Direct match with A908334 by name and address with minor variations.      |
| A911498    | TONY A MARTENS            | 31532 Vintners Pointe Ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Direct match with A952559 by name and address with minor variations.      |
| A952559    | ANTHONY A MARTENS         | 31532 vintners pointe ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Direct match with A911498 by name and address with minor variations.      |
| A943900    | matthew l ford            | 6512 CCLEON AVENUE                | NORTH HOLLYIWOOD     | CA    | 91606   | 021-48-0375 | NaN           | Direct match with A946676 by name and SSN with minor variations.          |
| A946676    | MATTHEW L FORD             | 6460 Charleston Court             | MILTON              | FL    | 32570   | 21480375    | NaN           | Direct match with A943900 by name and SSN with minor variations.          |
| B935222    | MATTHEW L                 | FORD                              | charleston ct        | NaN   | 32570   | 850.843.5125| NaN           | Direct match with B985964 by name and address with minor variations.      |
| B985964    | matthew L                 | FORD                              | cleonx ave           | ca    | 91606   | (818)425.4306| NaN           | Direct match with B935222 by name and address with minor variations.      |
| A920094    | FELICIA CRNELISSEN        | 1209 AUGUST WAY                   | Antioch             | Ca    | 94509   | 25047736    | NaN           | Direct match with A925218 by SSN with minor variations.                    |
| A925218    | CORNELISSEN               | 2049 SANTA CRUZ AQVENUE           | menlo park           | ca    | 94025   | 25407736    | NaN           | Direct match with A920094 by SSN with minor variations.                    |
| A930348    | JOYCE M PALLETT           | 7505 brighten dr                  | Tampa                | La.   | 33615   | NaN         | NaN           | Direct match with A939278 by name and address with minor variations.       |
| A939278    | M PALLETT                 | 7505 BRIGHTEN DRIVE               | tampa                | fl    | 33615   | NaN         | NaN           | Direct match with A930348 by name and address with minor variations.       |
| A911498    | TONY A MARTENS            | 31532 Vintners Pointe Ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Direct match with A925808 by name with minor variations.                  |
| A925808    | tony a martens            | 1213 w l st                       | WILMINTON           | CA    | 90744   | 022-10-2034 | NaN           | Direct match with A911498 by name with minor variations.                  |
| A909873    | M Y Kelley                | 5178 Nw Rugby Dr                  | PORT SAINT LUCIE     | FL    | 34983   | 26685998    | NaN           | Direct match with A915730 by name with minor variations.                  |
| A915730    | MILTON Y KELLEY           | 4300 BORDEAUX DRV                 | OAKLEY               | CA    | 9451    | 026-65-8998 | NaN           | Direct match with A909873 by name with minor variations.                  |
| B967576    | MARILYN J                 | KELLER                            | 515 W Park Dr        | apt 5 | MIAMI   | 33172       | 305-652-1001 | Direct match with B975893 by name with minor variations.                  |
| B975893    | MARY J                    | Keller                           | 1482 CALLER           | hawthorne | ca      | 90251       | 424-466-4517 | Direct match with B967576 by name with minor variations.                  |

#### Indirect Matching

| Record ID | Name                      | Address                           | City                | State | ZIP     | SSN         | Phone Number  | Explanation                                                                 |
|------------|---------------------------|-----------------------------------|---------------------|-------|---------|-------------|---------------|-----------------------------------------------------------------------------|
| A908334    | ANTHONY A MATRENS         | 521 COCHRAN AVEN                  | SAN DIEGTO          | CA    | 92154   | 202100234   | NaN           | Indirect match with A911498 and A952559 through name and address variations.|
| A911498    | TONY A MARTENS            | 31532 Vintners Pointe Ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Indirect match with A908334 and A952559 through name and address variations.|
| A952559    | ANTHONY A MARTENS         | 31532 vintners pointe ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Indirect match with A908334 and A911498 through name and address variations.|
| A943900    | matthew l ford            | 6512 CCLEON AVENUE                | NORTH HOLLYIWOOD     | CA    | 91606   | 021-48-0375 | NaN           | Indirect match with A946676 and B935222 through name and SSN variations.    |
| A946676    | MATTHEW L FORD             | 6460 Charleston Court             | MILTON              | FL    | 32570   | 21480375    | NaN           | Indirect match with A943900 and B935222 through name and SSN variations.    |
| B935222    | MATTHEW L                 | FORD                              | charleston ct        | NaN   | 32570   | 850.843.5125| NaN           | Indirect match with A943900 and A946676 through name and SSN variations.    |
| A920094    | FELICIA CRNELISSEN        | 1209 AUGUST WAY                   | Antioch             | Ca    | 94509   | 25047736    | NaN           | Indirect match with A925218 through SSN variations.                          |
| A925218    | CORNELISSEN               | 2049 SANTA CRUZ AQVENUE           | menlo park           | ca    | 94025   | 25407736    | NaN           | Indirect match with A920094 through SSN variations.                          |
| A930348    | JOYCE M PALLETT           | 7505 brighten dr                  | Tampa                | La.   | 33615   | NaN         | NaN           | Indirect match with A939278 through address variations.                     |
| A939278    | M PALLETT                 | 7505 BRIGHTEN DRIVE               | tampa                | fl    | 33615   | NaN         | NaN           | Indirect match with A930348 through address variations.                     |
| A911498    | TONY A MARTENS            | 31532 Vintners Pointe Ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Indirect match with A925808 through name variations.                        |
| A925808    | tony a martens            | 1213 w l st                       | WILMINTON           | CA    | 90744   | 022-10-2034 | NaN           | Indirect match with A911498 through name variations.                        |
| A909873    | M Y Kelley                | 5178 Nw Rugby Dr                  | PORT SAINT LUCIE     | FL    | 34983   | 26685998    | NaN           | Indirect match with A915730 through name variations.                          |
| A915730    | MILTON Y KELLEY           | 4300 BORDEAUX DRV                 | OAKLEY               | CA    | 9451    | 026-65-8998 | NaN           | Indirect match with A909873 through name variations.                          |
| B967576    | MARILYN J                 | KELLER                            | 515 W Park Dr        | apt 5 | MIAMI   | 33172       | 305-652-1001 | Indirect match with B975893 through name variations.                        |
| B975893    | MARY J                    | Keller                           | 1482 CALLER           | hawthorne | ca      | 90251       | 424-466-4517 | Indirect match with B967576 through name variations.                        |

#### Identify Households

| Record ID | Name                      | Address                           | City                | State | ZIP     | SSN         | Phone Number  | Explanation                                                                 |
|------------|---------------------------|-----------------------------------|---------------------|-------|---------|-------------|---------------|-----------------------------------------------------------------------------|
| A908334    | ANTHONY A MATRENS         | 521 COCHRAN AVEN                  | SAN DIEGTO          | CA    | 92154   | 202100234   | NaN           | Household with A931754 by address.                                         |
| A931754    | TONY A MARTENS            | 521 Cochran Avn                   | San Diego           | Ca    | 92154   | 22100234    | NaN           | Household with A908334 by address.                                         |
| A911498    | TONY A MARTENS            | 31532 Vintners Pointe Ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Household with A952559 by address.                                         |
| A952559    | ANTHONY A MARTENS         | 31532 vintners pointe ct          | winchester          | ca    | 92596   | 22100234    | NaN           | Household with A911498 by address.                                         |
| A943900    | matthew l ford            | 6512 CCLEON AVENUE                | NORTH HOLLYIWOOD     | CA    | 91606   | 021-48-0375 | NaN           | Household with B985964 by address.                                          |
| B985964    | matthew L                 | FORD                              | cleonx ave           | ca    | 91606   | (818)425.4306| NaN           | Household with A943900 by address.                                          |
| A946676    | MATTHEW L FORD             | 6460 Charleston Court             | MILTON              | FL    | 32570   | 21480375    | NaN           | Household with B935222 by address.                                         |
| B935222    | MATTHEW L                 | FORD                              | charleston ct        | NaN   | 32570   | 850.843.5125| NaN           | Household with A946676 by address.                                         |
| A920094    | FELICIA CRNELISSEN        | 1209 AUGUST WAY                   | Antioch             | Ca    | 94509   | 25047736    | NaN           | Household with A925218 by address.                                          |
| A925218    | CORNELISSEN               | 2049 SANTA CRUZ AQVENUE           | menlo park           | ca    | 94025   | 25407736    | NaN           | Household with A920094 by address.                                          |
| A930348    | JOYCE M PALLETT           | 7505 brighten dr                  | Tampa                | La.   | 33615   | NaN         | NaN           | Household with A939278 by address.                                           |
| A939278    | M PALLETT                 | 7505 BRIGHTEN DRIVE               | tampa                | fl    | 33615   | NaN         | NaN           | Household with A930348 by address.                                           |
| A911498    | TONY A MARTENS            | 31532 Vintners

#
