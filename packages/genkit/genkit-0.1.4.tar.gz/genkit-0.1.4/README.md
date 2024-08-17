# GenKit

GenKit is a versatile Python package designed for generating various types of data. It includes functionality for generating phone numbers in different formats based on country codes. Whether you need a phone number for testing or other purposes, genkit simplifies the process by offering customizable options.

## Features

- **Phone Number Generation** : Generate phone numbers in formats specific to various countries.
- **Customizable** : Specify the country to get the appropriate phone number format.
- **Easy Integration** : Seamlessly integrate into your Python projects.
- **File Saving**: Save generated data to text files with timestamps for easy tracking.
- **Flexible Formats**: Return data as a list, dictionary, or plain string based on user preference.

## Installation

You can easily install genkit using pip. Run the following command to install it:

```
pip install genkit
```

## Usage

### Generating a Single Phone Number

You can generate a single phone number for a specified country. By default, it generates an Indian phone number.

```
from genkit import GenKit

# Generate a phone number for India (default)
print(GenKit.phonenumber())

# Generate a phone number for the US
print(GenKit.phonenumber("US"))

```

### Generating Multiple Phone Numbers

To generate multiple phone numbers, use the `n` parameter to specify the quantity. You can also specify the output format using the `type` parameter.

```
from genkit import GenKit

# Generate 5 phone numbers for India and return as a list
print(GenKit.phonenumber("IN", n=5, type="list"))

# Generate 3 phone numbers for the US and return as a dictionary
print(GenKit.phonenumber("US", n=3, type="dict"))
```

### Saving to a File

You can save the generated phone numbers to a text file. The file will be named `genkit_TIMESTAMP.txt`, where `TIMESTAMP` is the current timestamp.

```
from genkit import GenKit

# Generate 5 phone numbers for India and save to a file
GenKit.phonenumber("IN", n=5, save=True)

# Generate 3 phone numbers for the US in dictionary format and save to a file
GenKit.phonenumber("US", n=3, type="dict", save=True)

```

## Reference

Generates phone numbers based on the specified parameters.

##### Parameters:

* n (int): Number of phone numbers to generate. Default is 1.
* type (str): Output format. Can be "string" (default), "list", or "dict".
* save (bool): Whether to save the generated numbers to a file. Default is False.

##### **Returns:**

* If `type` is "string": A newline-separated string of phone numbers.
* If `type` is "list": A list of phone numbers.
* If `type` is "dict": A dictionary with a key "phone_numbers" containing the list of phone numbers.

### Example

```
result = GenKit.phonenumber("US", n=5, type="dict", save=True)
print(result)  # Output: {'phone_numbers': ['+1XXXXXXXXXX', '+1XXXXXXXXXX', ...]}
```

## Supported Countries

The following countries are supported for phone number generation. Use 2-digit ISO codes to generate:

| ISO Code | Country                                      | Phone Code |
| -------- | -------------------------------------------- | ---------- |
| AF       | Afghanistan                                  | +93        |
| AL       | Albania                                      | +355       |
| DZ       | Algeria                                      | +213       |
| AS       | American Samoa                               | +1-684     |
| AD       | Andorra                                      | +376       |
| AO       | Angola                                       | +244       |
| AI       | Anguilla                                     | +1-264     |
| AQ       | Antarctica                                   | +672       |
| AG       | Antigua and Barbuda                          | +1-268     |
| AR       | Argentina                                    | +54        |
| AM       | Armenia                                      | +374       |
| AW       | Aruba                                        | +297       |
| AU       | Australia                                    | +61        |
| AT       | Austria                                      | +43        |
| AZ       | Azerbaijan                                   | +994       |
| BS       | Bahamas                                      | +1-242     |
| BH       | Bahrain                                      | +973       |
| BD       | Bangladesh                                   | +880       |
| BB       | Barbados                                     | +1-246     |
| BY       | Belarus                                      | +375       |
| BE       | Belgium                                      | +32        |
| BZ       | Belize                                       | +501       |
| BJ       | Benin                                        | +229       |
| BM       | Bermuda                                      | +1-441     |
| BT       | Bhutan                                       | +975       |
| BO       | Bolivia                                      | +591       |
| BA       | Bosnia and Herzegovina                       | +387       |
| BW       | Botswana                                     | +267       |
| BV       | Bouvet Island                                | +47        |
| BR       | Brazil                                       | +55        |
| IO       | British Indian Ocean Territory               | +246       |
| BN       | Brunei                                       | +673       |
| BG       | Bulgaria                                     | +359       |
| BF       | Burkina Faso                                 | +226       |
| KH       | Cambodia                                     | +855       |
| CM       | Cameroon                                     | +237       |
| CA       | Canada                                       | +1         |
| CV       | Cape Verde                                   | +238       |
| KY       | Cayman Islands                               | +1-345     |
| CF       | Central African Republic                     | +236       |
| TD       | Chad                                         | +235       |
| CL       | Chile                                        | +56        |
| CN       | China                                        | +86        |
| CX       | Christmas Island                             | +61        |
| CC       | Cocos (Keeling) Islands                      | +61        |
| CO       | Colombia                                     | +57        |
| KM       | Comoros                                      | +269       |
| CD       | Congo, Democratic Republic of the            | +243       |
| CG       | Congo, Republic of the                       | +242       |
| CK       | Cook Islands                                 | +682       |
| CR       | Costa Rica                                   | +506       |
| CI       | Cote D'Ivoire                                | +225       |
| HR       | Croatia                                      | +385       |
| CU       | Cuba                                         | +53        |
| CY       | Cyprus                                       | +357       |
| CZ       | Czech Republic                               | +420       |
| CS       | Czechoslovakia                               | +42        |
| DK       | Denmark                                      | +45        |
| DJ       | Djibouti                                     | +253       |
| DM       | Dominica                                     | +1-767     |
| DO       | Dominican Republic                           | +1-809     |
| TP       | East Timor                                   | +670       |
| EC       | Ecuador                                      | +593       |
| EG       | Egypt                                        | +20        |
| SV       | El Salvador                                  | +503       |
| GQ       | Equatorial Guinea                            | +240       |
| ER       | Eritrea                                      | +291       |
| EE       | Estonia                                      | +372       |
| ET       | Ethiopia                                     | +251       |
| FK       | Falkland Islands                             | +500       |
| FO       | Faroe Islands                                | +298       |
| FJ       | Fiji                                         | +679       |
| FI       | Finland                                      | +358       |
| FR       | France                                       | +33        |
| GF       | French Guiana                                | +594       |
| PF       | French Polynesia                             | +689       |
| TF       | French Southern Territories                  | +262       |
| GA       | Gabon                                        | +241       |
| GM       | Gambia                                       | +220       |
| GE       | Georgia                                      | +995       |
| DE       | Germany                                      | +49        |
| GH       | Ghana                                        | +233       |
| GI       | Gibraltar                                    | +350       |
| GB       | United Kingdom                               | +44        |
| GR       | Greece                                       | +30        |
| GL       | Greenland                                    | +299       |
| GD       | Grenada                                      | +1-473     |
| GP       | Guadeloupe                                   | +590       |
| GU       | Guam                                         | +1-671     |
| GT       | Guatemala                                    | +502       |
| GN       | Guinea                                       | +224       |
| GW       | Guinea-Bissau                                | +245       |
| GY       | Guyana                                       | +592       |
| HT       | Haiti                                        | +509       |
| HM       | Heard Island and McDonald Islands            | +672       |
| VA       | Holy See (Vatican City State)                | +39        |
| HN       | Honduras                                     | +504       |
| HK       | Hong Kong                                    | +852       |
| HU       | Hungary                                      | +36        |
| IS       | Iceland                                      | +354       |
| IN       | India                                        | +91        |
| ID       | Indonesia                                    | +62        |
| IR       | Iran                                         | +98        |
| IQ       | Iraq                                         | +964       |
| IE       | Ireland                                      | +353       |
| IL       | Israel                                       | +972       |
| IT       | Italy                                        | +39        |
| JM       | Jamaica                                      | +1-876     |
| JP       | Japan                                        | +81        |
| JO       | Jordan                                       | +962       |
| KZ       | Kazakhstan                                   | +7         |
| KE       | Kenya                                        | +254       |
| KI       | Kiribati                                     | +686       |
| KP       | North Korea                                  | +850       |
| KR       | South Korea                                  | +82        |
| KW       | Kuwait                                       | +965       |
| KG       | Kyrgyzstan                                   | +996       |
| LA       | Laos                                         | +856       |
| LV       | Latvia                                       | +371       |
| LB       | Lebanon                                      | +961       |
| LS       | Lesotho                                      | +266       |
| LR       | Liberia                                      | +231       |
| LY       | Libya                                        | +218       |
| LI       | Liechtenstein                                | +423       |
| LT       | Lithuania                                    | +370       |
| LU       | Luxembourg                                   | +352       |
| MO       | Macau                                        | +853       |
| MK       | North Macedonia                              | +389       |
| MG       | Madagascar                                   | +261       |
| MW       | Malawi                                       | +265       |
| MY       | Malaysia                                     | +60        |
| MV       | Maldives                                     | +960       |
| ML       | Mali                                         | +223       |
| MT       | Malta                                        | +356       |
| MH       | Marshall Islands                             | +692       |
| MQ       | Martinique                                   | +596       |
| MR       | Mauritania                                   | +222       |
| MU       | Mauritius                                    | +230       |
| YT       | Mayotte                                      | +269       |
| MX       | Mexico                                       | +52        |
| FM       | Micronesia                                   | +691       |
| MD       | Moldova                                      | +373       |
| MC       | Monaco                                       | +377       |
| MN       | Mongolia                                     | +976       |
| MS       | Montserrat                                   | +1-664     |
| MA       | Morocco                                      | +212       |
| MZ       | Mozambique                                   | +258       |
| MM       | Myanmar                                      | +95        |
| NA       | Namibia                                      | +264       |
| NR       | Nauru                                        | +674       |
| NP       | Nepal                                        | +977       |
| NL       | Netherlands                                  | +31        |
| AN       | Netherlands Antilles                         | +599       |
| NC       | New Caledonia                                | +687       |
| NZ       | New Zealand                                  | +64        |
| NI       | Nicaragua                                    | +505       |
| NE       | Niger                                        | +227       |
| NG       | Nigeria                                      | +234       |
| NU       | Niue                                         | +683       |
| NF       | Norfolk Island                               | +672       |
| MP       | Northern Mariana Islands                     | +1-670     |
| NO       | Norway                                       | +47        |
| OM       | Oman                                         | +968       |
| PK       | Pakistan                                     | +92        |
| PW       | Palau                                        | +680       |
| PS       | Palestine                                    | +970       |
| PA       | Panama                                       | +507       |
| PG       | Papua New Guinea                             | +675       |
| PY       | Paraguay                                     | +595       |
| PE       | Peru                                         | +51        |
| PH       | Philippines                                  | +63        |
| PN       | Pitcairn                                     | +870       |
| PL       | Poland                                       | +48        |
| PT       | Portugal                                     | +351       |
| PR       | Puerto Rico                                  | +1-787     |
| QA       | Qatar                                        | +974       |
| RE       | Reunion                                      | +262       |
| RO       | Romania                                      | +40        |
| RU       | Russia                                       | +7         |
| RW       | Rwanda                                       | +250       |
| BL       | Saint Barthelemy                             | +590       |
| SH       | Saint Helena                                 | +290       |
| KN       | Saint Kitts and Nevis                        | +1-869     |
| LC       | Saint Lucia                                  | +1-758     |
| MF       | Saint Martin                                 | +590       |
| PM       | Saint Pierre and Miquelon                    | +508       |
| VC       | Saint Vincent and the Grenadines             | +1-784     |
| WS       | Samoa                                        | +685       |
| SM       | San Marino                                   | +378       |
| ST       | Sao Tome and Principe                        | +239       |
| SA       | Saudi Arabia                                 | +966       |
| SN       | Senegal                                      | +221       |
| SC       | Seychelles                                   | +248       |
| SL       | Sierra Leone                                 | +232       |
| SG       | Singapore                                    | +65        |
| SX       | Sint Maarten                                 | +1-721     |
| SK       | Slovakia                                     | +421       |
| SI       | Slovenia                                     | +386       |
| SB       | Solomon Islands                              | +677       |
| SO       | Somalia                                      | +252       |
| ZA       | South Africa                                 | +27        |
| GS       | South Georgia and the South Sandwich Islands | +500       |
| SS       | South Sudan                                  | +211       |
| ES       | Spain                                        | +34        |
| LK       | Sri Lanka                                    | +94        |
| SD       | Sudan                                        | +249       |
| SR       | Suriname                                     | +597       |
| SZ       | Swaziland                                    | +268       |
| SE       | Sweden                                       | +46        |
| CH       | Switzerland                                  | +41        |
| SY       | Syria                                        | +963       |
| TW       | Taiwan                                       | +886       |
| TJ       | Tajikistan                                   | +992       |
| TZ       | Tanzania                                     | +255       |
| TH       | Thailand                                     | +66        |
| TL       | Timor-Leste                                  | +670       |
| TG       | Togo                                         | +228       |
| TK       | Tokelau                                      | +690       |
| TO       | Tonga                                        | +676       |
| TT       | Trinidad and Tobago                          | +1-868     |
| TN       | Tunisia                                      | +216       |
| TR       | Turkey                                       | +90        |
| TM       | Turkmenistan                                 | +993       |
| TV       | Tuvalu                                       | +688       |
| UG       | Uganda                                       | +256       |
| UA       | Ukraine                                      | +380       |
| AE       | United Arab Emirates                         | +971       |
| GB       | United Kingdom                               | +44        |
| US       | United States                                | +1         |
| UY       | Uruguay                                      | +598       |
| UZ       | Uzbekistan                                   | +998       |
| VU       | Vanuatu                                      | +678       |
| VE       | Venezuela                                    | +58        |
| VN       | Vietnam                                      | +84        |
| VG       | Virgin Islands (British)                     | +1-284     |
| VI       | Virgin Islands (U.S.)                        | +1-340     |
| WF       | Wallis and Futuna                            | +681       |
| EH       | Western Sahara                               | +212       |
| YE       | Yemen                                        | +967       |
| ZM       | Zambia                                       | +260       |
| ZW       | Zimbabwe                                     | +263       |

## Authors

For any questions or issues, please contact:

* **Author** : [Suhail Shaji](https://github.com/suhailshaji)
* **Email** : [suhailshaji@gmail.com]()

## Feedback

If you have any feedback, please reach out to us at
suhailshaji@gmail.com

## License

[MIT](https://choosealicense.com/licenses/mit/)

## 🔗 Connect

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/suhailshaji)
