# jhuregionmapper
Maps Johns Hopkins University COVID-19 regions to iso country and region code and Wikidata Entity Ids

see https://github.com/CSSEGISandData/COVID-19/issues/1908

# Installation
The software is written in Python and uses JanusGraph and Apache Tinkerpop

see http://wiki.bitplan.com/index.php/Gremlin_python

To start your janusgraph 

`docker run -it -p 8182:8182 --mount src=<path to graphdata>,target=/graphdata,type=bind janusgraph/janusgraph`

e.g.
`docker run -it -p 8182:8182 --mount src=/bitplan/user/wf/graphdata,target=/graphdata,type=bind janusgraph/janusgraph`

in my environment i am running janusgraph on our ubuntu server so that /bitplan/user/wf/graphdata is accessible from my Mac OS machine via /Volumes/bitplan/user/wf/graphdata

When first run the region information is cached in a graphml file region.xml which takes roughly a minute to create.
Later the region data is read from the graphml based tinkerpop graphdatabase.

The matching result currently works for the global data for some 251 regions.
<pre>
✅            Afghanistan                        33.0,  65.0 -  145 km->    AF;     Q889;                             Afghanistan; 34940837;  34.0;  66.0
✅                Albania                        41.2,  20.2 -   22 km->    AL;     Q222;                                 Albania;  3020209;  41.0;  20.0
✅                Algeria                        28.0,   1.7 -   65 km->    DZ;     Q262;                                 Algeria; 41318142;  28.0;   1.0
✅                Andorra                        42.5,   1.5 -    6 km->    AD;     Q228;                                 Andorra;    76177;  42.6;   1.6
✅                 Angola                       -11.2,  17.9 -  139 km->    AO;     Q916;                                  Angola; 29784193; -12.3;  17.4
✅    Antigua and Barbuda                        17.1, -61.8 -    8 km->    AG;     Q781;                     Antigua and Barbuda;   102012;  17.1; -61.9
✅              Argentina                       -38.4, -63.6 -  491 km->    AR;     Q414;                               Argentina; 44938712; -34.0; -64.0
✅                Armenia                        40.1,  45.0 -   36 km->    AM;     Q399;                                 Armenia;  2930450;  40.4;  45.0
✅              Australia Australian Capital Territory  -35.5, 149.0 -    4 km->AU-ACT;    Q3258;            Australian Capital Territory;   396857; -35.5; 149.0
✅              Australia      New South Wales  -33.9, 151.2 -    0 km->AU-NSW;    Q3224;                         New South Wales;  7480228; -32.0; 147.0
✅              Australia   Northern Territory  -12.5, 130.8 -    0 km-> AU-NT;    Q3235;                      Northern Territory;   245562; -20.0; 133.0
✅              Australia           Queensland  -28.0, 153.4 -    0 km->AU-QLD;   Q36074;                              Queensland;  4703193; -20.0; 143.0
✅              Australia      South Australia  -34.9, 138.6 -    0 km-> AU-SA;   Q35715;                         South Australia;  1676653; -30.0; 135.0
✅              Australia             Tasmania  -41.5, 146.0 -  105 km->AU-TAS;   Q34366;                                Tasmania;   509965; -42.0; 147.0
✅              Australia             Victoria  -37.8, 145.0 -  124 km->AU-VIC;   Q36687;                                Victoria;  5926624; -37.0; 144.0
✅              Australia    Western Australia  -32.0, 115.9 -  828 km-> AU-WA;    Q3206;                       Western Australia;  2474410; -26.0; 121.0
✅                Austria                        47.5,  14.6 -   68 km->    AT;      Q40;                                 Austria;  8809212;  48.0;  14.0
✅             Azerbaijan                        40.1,  47.6 -   20 km->    AZ;     Q227;                              Azerbaijan; 10000000;  40.3;  47.7
✅                Bahamas                        25.0, -77.4 -  179 km->    BS;     Q778;                                 Bahamas;   395361;  23.7; -76.4
✅                Bahrain                        26.0,  50.5 -    4 km->    BH;     Q398;                                 Bahrain;  1492584;  26.1;  50.6
✅             Bangladesh                        23.7,  90.4 -   62 km->    BD;     Q902;                              Bangladesh;164669751;  24.0;  89.9
✅               Barbados                        13.2, -59.5 -    3 km->    BB;     Q244;                                Barbados;   285719;  13.2; -59.6
✅                Belarus                        53.7,  28.0 -   21 km->    BY;     Q184;                                 Belarus;  9494200;  53.5;  28.0
✅                Belgium                        50.8,   4.0 -   52 km->    BE;      Q31;                                 Belgium; 11431406;  50.6;   4.7
✅                  Benin                         9.3,   2.3 -   54 km->    BJ;     Q962;                                   Benin; 11175692;   8.8;   2.2
✅                 Bhutan                        27.5,  90.4 -   10 km->    BT;     Q917;                                  Bhutan;   807610;  27.4;  90.5
✅                Bolivia                       -16.3, -63.6 -  172 km->    BO;     Q750;                                 Bolivia; 11051600; -17.1; -65.0
✅ Bosnia and Herzegovina                        43.9,  17.7 -   27 km->    BA;     Q225;                  Bosnia and Herzegovina;  3507017;  44.0;  18.0
✅                 Brazil                       -14.2, -51.9 -  119 km->    BR;     Q155;                                  Brazil;208494900; -14.0; -53.0
✅                 Brunei                         4.5, 114.7 -   23 km->    BN;     Q921;                                  Brunei;   417784;   4.4; 114.6
✅               Bulgaria                        42.7,  25.5 -    2 km->    BG;     Q219;                                Bulgaria;  7000039;  42.8;  25.5
✅           Burkina Faso                        12.2,  -1.6 -   55 km->    BF;     Q965;                            Burkina Faso; 19193382;  12.3;  -2.1
✅             Cabo Verde                        16.5, -23.0 -    0 km->    CV;    Q1011;                              Cape Verde;   546388;  15.9; -24.1
✅               Cambodia                        11.6, 104.9 -  117 km->    KH;     Q424;                                Cambodia; 15135169;  12.6; 105.0
✅               Cameroon                         3.8,  11.5 -    0 km->    CM;    Q1009;                                Cameroon; 24053727;   7.0;  12.0
✅                 Canada              Alberta   53.9,-116.6 -  157 km-> CA-AB;    Q1951;                                 Alberta;  4067175;  55.0;-115.0
✅                 Canada     British Columbia   49.3,-123.1 -    0 km-> CA-BC;    Q1974;                        British Columbia;  4841078;  54.5;-124.5
✅                 Canada       Grand Princess   37.6,-122.7 -    0 km-> US-CA;      Q99;                              California; 39144818;  37.0;-120.0
✅                 Canada             Manitoba   53.8, -98.8 -  181 km-> CA-MB;    Q1948;                                Manitoba;  1343371;  55.0; -97.0
✅                 Canada        New Brunswick   46.6, -66.5 -   36 km-> CA-NB;    Q1965;                           New Brunswick;   760868;  46.6; -66.0
✅                 Canada Newfoundland and Labrador   53.1, -57.7 -  158 km-> CA-NL;    Q2003;               Newfoundland and Labrador;   528430;  53.0; -60.0
✅                 Canada          Nova Scotia   44.7, -63.7 -   69 km-> CA-NS;    Q1952;                             Nova Scotia;   957600;  45.0; -63.0
✅                 Canada              Ontario   51.3, -85.3 -  141 km-> CA-ON;    Q1904;                                 Ontario; 14279196;  50.0; -85.0
✅                 Canada Prince Edward Island   46.5, -63.4 -   43 km-> CA-PE;    Q1979;                    Prince Edward Island;   152784;  46.2; -63.0
✅                 Canada               Quebec   52.9, -73.5 -  148 km-> CA-QC;     Q176;                                  Quebec;  8484965;  52.0; -72.0
✅                 Canada         Saskatchewan   52.9,-106.5 -  231 km-> CA-SK;    Q1989;                            Saskatchewan;  1168057;  55.0;-106.0
✅ Central African Republic                         6.6,  20.9 -   11 km->    CF;     Q929;                Central African Republic;  4659080;   6.7;  20.9
✅                   Chad                        15.5,  18.7 -   72 km->    TD;     Q657;                                    Chad; 15477751;  15.5;  19.4
✅                  Chile                       -35.7, -71.5 -  301 km->    CL;     Q298;                                   Chile; 18054726; -33.0; -71.0
✅                  China                Anhui   31.8, 117.2 -   21 km-> CN-AH;   Q40956;                                   Anhui;       -1;  31.8; 117.0
✅                  China              Beijing   40.2, 116.4 -    0 km->    CN;     Q148;              People's Republic of China;1409517397;  35.0; 103.0
✅                  China            Chongqing   30.1, 107.9 -    0 km-> CN-SC;   Q19770;                                 Sichuan; 81100000;  30.0; 103.0
✅                  China               Fujian   26.1, 118.0 -   37 km-> CN-FJ;   Q41705;                                  Fujian; 36894216;  25.9; 118.3
✅                  China                Gansu   37.8, 101.1 -   85 km-> CN-GS;   Q42392;                                   Gansu; 25575254;  38.0; 102.0
✅                  China            Guangdong   23.3, 113.4 -   10 km-> CN-GD;   Q15175;                               Guangdong;       -1;  23.4; 113.5
✅                  China              Guangxi   23.8, 108.8 -   56 km-> CN-GX;   Q15176;        Guangxi Zhuang Autonomous Region; 46026629;  23.6; 108.3
✅                  China              Guizhou   26.8, 106.9 -    5 km-> CN-GZ;   Q47097;                                 Guizhou;       -1;  26.8; 106.8
✅                  China               Hainan   19.2, 109.7 -  111 km-> CN-HI;   Q42200;                                  Hainan;  9171300;  20.0; 110.3
✅                  China                Hebei   39.5, 116.1 -  219 km-> CN-HE;   Q21208;                                   Hebei; 71854202;  38.0; 114.5
✅                  China         Heilongjiang   47.9, 127.8 -   94 km-> CN-HL;   Q19206;                            Heilongjiang; 38312224;  48.0; 129.0
✅                  China                Henan   33.9, 113.6 -   11 km-> CN-HA;   Q43684;                                   Henan;       -1;  33.9; 113.5
✅                  China            Hong Kong   22.3, 114.2 -    5 km-> CN-HK;    Q8646;                               Hong Kong;  7500700;  22.3; 114.2
✅                  China                Hubei   31.0, 112.3 -   25 km-> CN-HB;   Q46862;                                   Hubei; 58160000;  31.2; 112.3
✅                  China                Hunan   27.6, 111.7 -   25 km-> CN-HN;   Q45761;                                   Hunan; 65683722;  27.4; 111.8
✅                  China       Inner Mongolia   44.1, 113.9 -   76 km-> CN-NM;   Q41079;                          Inner Mongolia; 24706321;  44.0; 113.0
✅                  China              Jiangsu   33.0, 119.5 -   51 km-> CN-JS;   Q16963;                                 Jiangsu; 78659903;  33.0; 120.0
✅                  China              Jiangxi   27.6, 115.7 -   44 km-> CN-JX;   Q57052;                                 Jiangxi; 44567475;  27.3; 116.0
✅                  China                Jilin   43.7, 126.2 -   75 km-> CN-JL;   Q45208;                                   Jilin; 27462297;  43.9; 125.3
✅                  China             Liaoning   41.3, 122.6 -   89 km-> CN-LN;   Q43934;                                Liaoning; 43746323;  41.8; 123.4
✅                  China                Macau   22.2, 113.5 -    0 km-> CN-MO;   Q14773;                                   Macau;   566375;  22.2; 113.5
✅                  China              Ningxia   37.3, 106.2 -    0 km-> CN-NX;   Q57448;           Ningxia Hui Autonomous Region;  6301350;  38.5; 106.3
✅                  China              Qinghai   35.7,  96.0 -   83 km-> CN-QH;   Q45833;                                 Qinghai;  5930000;  35.0;  96.0
✅                  China              Shaanxi   35.2, 108.9 -  103 km-> CN-SN;   Q47974;                                 Shaanxi; 37327378;  34.3; 108.9
✅                  China             Shandong   36.3, 118.1 -   23 km-> CN-SD;   Q43407;                                Shandong; 95793065;  36.4; 118.4
✅                  China             Shanghai   31.2, 121.4 -    0 km->    CN;     Q148;              People's Republic of China;1409517397;  35.0; 103.0
✅                  China               Shanxi   37.6, 112.3 -   41 km-> CN-SX;   Q46913;                                  Shanxi; 36500000;  37.9; 112.6
✅                  China              Sichuan   30.6, 102.7 -   74 km-> CN-SC;   Q19770;                                 Sichuan; 81100000;  30.0; 103.0
✅                  China              Tianjin   39.3, 117.3 -    0 km-> CN-HE;   Q21208;                                   Hebei; 71854202;  38.0; 114.5
✅                  China                Tibet   31.7,  88.1 -    0 km-> CN-XZ;   Q17269;                 Tibet Autonomous Region;  3180000;  31.7;  86.9
✅                  China             Xinjiang   41.1,  85.2 -  359 km-> CN-XJ;   Q34800;                                Xinjiang; 21813334;  43.8;  87.6
✅                  China               Yunnan   25.0, 101.5 -   53 km-> CN-YN;   Q43194;                                  Yunnan;       -1;  24.5; 101.5
✅                  China             Zhejiang   29.2, 120.1 -  120 km-> CN-ZJ;   Q16967;                                Zhejiang; 56570000;  30.3; 120.2
✅               Colombia                         4.6, -74.3 -   71 km->    CO;     Q739;                                Colombia; 49065615;   4.0; -74.0
✅    Congo (Brazzaville)                        -4.0,  21.8 -    0 km->    CD;     Q974;        Democratic Republic of the Congo; 86790567;  -2.9;  23.7
✅       Congo (Kinshasa)                        -4.0,  21.8 -    0 km->    CD;     Q974;        Democratic Republic of the Congo; 86790567;  -2.9;  23.7
✅             Costa Rica                         9.7, -83.8 -   39 km->    CR;     Q800;                              Costa Rica;  4905769;  10.0; -84.0
✅          Cote d'Ivoire                         7.5,  -5.5 -   71 km->    CI;    Q1008;                             Ivory Coast; 20316086;   8.0;  -6.0
✅                Croatia                        45.1,  15.2 -   27 km->    HR;     Q224;                                 Croatia;  4105493;  45.2;  15.5
✅                   Cuba                        22.0, -80.0 -   52 km->    CU;     Q241;                                    Cuba; 11484636;  22.0; -79.5
✅                 Cyprus                        35.1,  33.4 -   42 km->    CY;     Q229;                      Republic of Cyprus;  1141166;  35.0;  33.0
✅                Czechia                        49.8,  15.5 -   43 km->    CZ;     Q213;                          Czech Republic; 10649800;  50.0;  16.0
✅                Denmark        Faroe Islands   61.9,  -6.9 -    9 km->    FO;    Q4628;                           Faroe Islands;    49854;  62.0;  -6.8
✅                Denmark            Greenland   71.7, -42.6 -    0 km->    GL;     Q223;                               Greenland;    56081;  72.0; -40.0
✅                Denmark                        56.3,   9.5 -   43 km->    DK;      Q35;                                 Denmark;  5827463;  56.0;  10.0
✅               Djibouti                        11.8,  42.6 -   17 km->    DJ;     Q977;                                Djibouti;   956985;  11.8;  42.4
✅     Dominican Republic                        18.7, -70.2 -    8 km->    DO;     Q786;                      Dominican Republic; 10403761;  18.8; -70.2
✅                Ecuador                        -1.8, -78.2 -   94 km->    EC;     Q736;                                 Ecuador; 15737878;  -1.0; -78.0
✅                  Egypt                        26.0,  30.0 -  149 km->    EG;      Q79;                                   Egypt; 94798827;  27.0;  29.0
✅            El Salvador                        13.8, -88.9 -   14 km->    SV;     Q792;                             El Salvador;  6420746;  13.7; -88.9
✅      Equatorial Guinea                         1.5,  10.0 -    0 km->    GQ;     Q983;                       Equatorial Guinea;  1267689;   1.5;  10.0
✅                Eritrea                        15.2,  39.8 -  168 km->    ER;     Q986;                                 Eritrea;  3497000;  15.5;  38.2
✅                Estonia                        58.6,  25.0 -   73 km->    EE;     Q191;                                 Estonia;  1324820;  59.0;  26.0
✅               Eswatini                       -26.5,  31.5 -    5 km->    SZ;    Q1050;                                Eswatini;  1367254; -26.5;  31.4
✅               Ethiopia                         9.1,  40.5 -   56 km->    ET;     Q115;                                Ethiopia;104957438;   9.0;  40.0
✅                   Fiji                       -17.7, 178.1 -   32 km->    FJ;     Q712;                                    Fiji;   905502; -18.0; 178.0
✅                Finland                        64.0,  26.0 -  121 km->    FI;      Q33;                                 Finland;  5501043;  65.0;  27.0
✅                 France        French Guiana    3.9, -53.1 -   16 km-> FR-GF;    Q3769;                           French Guiana;   268700;   4.0; -53.0
✅                 France     French Polynesia  -17.7, 149.4 -    0 km-> FR-PF;   Q30971;                        French Polynesia;   275918; -17.5;-149.6
✅                 France           Guadeloupe   16.2, -61.6 -    0 km-> FR-GP;   Q17012;                              Guadeloupe;   390253;  16.2; -61.6
✅                 France              Mayotte  -12.8,  45.2 -    3 km-> FR-YT;   Q17063;                                 Mayotte;   256518; -12.8;  45.1
✅                 France        New Caledonia  -20.9, 165.6 -   51 km-> FR-NC;   Q33788;                           New Caledonia;   278500; -21.2; 165.3
✅                 France              Reunion  -21.1,  55.2 -   30 km-> FR-RE;   Q17070;                                 Réunion;   853659; -21.1;  55.5
✅                 France     Saint Barthelemy   17.9, -62.8 -    0 km-> FR-BL;   Q25362;                        Saint Barthélemy;     9625;  17.9; -62.8
✅                 France            St Martin   18.1, -63.1 -    1 km-> FR-MF;  Q126125;                            Saint Martin;    35684;  18.1; -63.1
✅                 France           Martinique   14.6, -61.0 -    4 km-> FR-MQ;   Q17054;                              Martinique;   372594;  14.7; -61.0
✅                 France                        46.2,   2.2 -   87 km->    FR;     Q142;                                  France; 66628000;  47.0;   2.0
✅                  Gabon                        -0.8,  11.6 -   18 km->    GA;    Q1000;                                   Gabon;  2025137;  -0.7;  11.5
✅                 Gambia                        13.4, -15.3 -   22 km->    GM;    Q1005;                                  Gambia;  2100568;  13.5; -15.5
✅                Georgia                        42.3,  43.4 -   45 km->    GE;     Q230;                                 Georgia;  3717100;  42.0;  43.7
✅                Germany                        51.0,   9.0 -    0 km->    DE;     Q183;                                 Germany; 83149300;  51.0;  10.0
✅                  Ghana                         7.9,  -1.0 -   58 km->    GH;     Q117;                                   Ghana; 26908262;   8.0;  -0.5
✅                 Greece                        39.1,  21.8 -  120 km->    GR;      Q41;                                  Greece; 10760421;  38.5;  23.0
✅              Guatemala                        15.8, -90.2 -   31 km->    GT;     Q774;                               Guatemala; 15468203;  15.5; -90.2
✅                 Guinea                         9.9,  -9.7 -  143 km->    GN;    Q1006;                                  Guinea; 11628972;  10.0; -11.0
✅                 Guyana                         5.0, -58.8 -  103 km->    GY;     Q734;                                  Guyana;   777859;   5.7; -59.3
✅                  Haiti                        19.0, -72.3 -   54 km->    HT;     Q790;                                   Haiti; 10317461;  19.0; -72.8
✅               Holy See                        41.9,  12.5 -    0 km->    VA;     Q237;                            Vatican City;     1000;  41.9;  12.5
✅               Honduras                        15.2, -86.2 -   88 km->    HN;     Q783;                                Honduras;  8097688;  14.6; -86.8
✅                Hungary                        47.2,  19.5 -   42 km->    HU;      Q28;                                 Hungary;  9971727;  47.0;  19.0
✅                Iceland                        65.0, -19.0 -    4 km->    IS;     Q189;                                 Iceland;   357050;  65.0; -19.0
✅                  India                        21.0,  78.0 -  152 km->    IN;     Q668;                                   India;1349217956;  22.0;  77.0
✅              Indonesia                        -0.8, 113.9 -  473 km->    ID;     Q252;                               Indonesia;263991379;  -2.0; 118.0
✅                   Iran                        32.0,  53.0 -    0 km->    IR;     Q794;                                    Iran; 79966230;  32.0;  53.0
✅                   Iraq                        33.0,  44.0 -   93 km->    IQ;     Q796;                                    Iraq; 38274618;  33.0;  43.0
✅                Ireland                        53.1,  -7.7 -   26 km->    IE;      Q27;                                 Ireland;  4761865;  53.0;  -8.0
✅                 Israel                        31.0,  35.0 -    0 km->    IL;     Q801;                                  Israel;  8891800;  31.0;  35.0
✅                  Italy                        43.0,  12.0 -   69 km->    IT;      Q38;                                   Italy; 60599936;  42.5;  12.5
✅                Jamaica                        18.1, -77.3 -   13 km->    JM;     Q766;                                 Jamaica;  2890299;  18.2; -77.4
✅                  Japan                        36.0, 138.0 -  213 km->    JP;      Q17;                                   Japan;127110047;  35.0; 136.0
✅                 Jordan                        31.2,  36.5 -    5 km->    JO;     Q810;                                  Jordan; 10428241;  31.2;  36.5
✅             Kazakhstan                        48.0,  66.9 -   80 km->    KZ;     Q232;                              Kazakhstan; 18276500;  48.0;  68.0
✅                  Kenya                        -0.0,  37.9 -   17 km->    KE;     Q114;                                   Kenya; 48468138;   0.1;  38.0
✅           Korea, South                        36.0, 128.0 -    0 km->    KR;     Q884;                             South Korea; 51069375;  36.0; 128.0
✅                 Kuwait                        29.5,  47.8 -   40 km->    KW;     Q817;                                  Kuwait;  4660000;  29.2;  47.6
✅             Kyrgyzstan                        41.2,  74.8 -   30 km->    KG;     Q813;                              Kyrgyzstan;  6201500;  41.0;  75.0
✅                 Latvia                        56.9,  24.6 -   28 km->    LV;     Q211;                                  Latvia;  1953000;  57.0;  25.0
✅                Lebanon                        33.9,  35.9 -    9 km->    LB;     Q822;                                 Lebanon;  6100075;  33.8;  35.8
✅                Liberia                         6.4,  -9.4 -   37 km->    LR;    Q1014;                                 Liberia;  4731906;   6.5;  -9.8
✅          Liechtenstein                        47.1,   9.6 -    1 km->    LI;     Q347;                           Liechtenstein;    37922;  47.1;   9.6
✅              Lithuania                        55.2,  23.9 -    8 km->    LT;      Q37;                               Lithuania;  2790842;  55.2;  24.0
✅             Luxembourg                        49.8,   6.1 -    5 km->    LU;      Q32;                              Luxembourg;   626108;  49.8;   6.1
✅             Madagascar                       -18.8,  46.9 -  137 km->    MG;    Q1019;                              Madagascar; 25570895; -20.0;  47.0
✅               Malaysia                         2.5, 112.5 -    0 km->    MY;     Q833;                                Malaysia; 31624264;   3.0; 108.0
✅               Maldives                         3.2,  73.2 -    0 km->    MV;     Q826;                                Maldives;   436330;   3.2;  73.2
✅                  Malta                        35.9,  14.4 -   13 km->    MT;     Q233;                                   Malta;   465292;  35.9;  14.5
✅             Mauritania                        21.0,  10.9 -    0 km->    MR;    Q1025;                              Mauritania;  4420184;  21.0; -11.0
✅              Mauritius                       -20.2,  57.5 -    0 km->    MU;    Q1027;                               Mauritius;  1264613; -20.2;  57.5
✅                 Mexico                        23.6,-102.6 -   90 km->    MX;      Q96;                                  Mexico;130526945;  23.0;-102.0
✅                Moldova                        47.4,  28.4 -   21 km->    MD;     Q217;                                 Moldova;  2550900;  47.2;  28.5
✅                 Monaco                        43.7,   7.4 -    0 km->    MC;     Q235;                                  Monaco;    37831;  43.7;   7.4
✅               Mongolia                        46.9, 103.8 -   19 km->    MN;     Q711;                                Mongolia;  3081678;  47.0; 104.0
✅             Montenegro                        42.5,  19.3 -   30 km->    ME;     Q236;                              Montenegro;   622359;  42.8;  19.2
✅                Morocco                        31.8,  -7.1 -  106 km->    MA;    Q1028;                                 Morocco; 36029138;  32.0;  -6.0
✅                Namibia                       -23.0,  18.5 -  153 km->    NA;    Q1030;                                 Namibia;  2303315; -23.0;  17.0
✅                  Nepal                        28.2,  84.2 -   31 km->    NP;     Q837;                                   Nepal; 29400000;  28.0;  84.0
✅            Netherlands                Aruba   12.5, -70.0 -    7 km-> NL-AW;   Q21203;                                   Aruba;   102911;  12.5; -70.0
✅            Netherlands              Curacao   12.2, -69.0 -    3 km-> NL-CW;   Q25279;                                 Curaçao;   160337;  12.2; -69.0
✅            Netherlands         Sint Maarten   18.0, -63.1 -    2 km-> NL-SX;   Q26273;                            Sint Maarten;    37132;  18.0; -63.1
✅            Netherlands                        52.1,   5.3 -    0 km->    NL;   Q29999;              Kingdom of the Netherlands; 17100715;  52.4;   4.9
✅            New Zealand                       -40.9, 174.9 -   82 km->    NZ;     Q664;                             New Zealand;  4885300; -41.2; 174.0
✅              Nicaragua                        12.9, -85.2 -   27 km->    NI;     Q811;                               Nicaragua;  6217581;  13.0; -85.0
✅                  Niger                        17.6,   8.1 -  215 km->    NE;    Q1032;                                   Niger; 21477348;  17.0;  10.0
✅                Nigeria                         9.1,   8.7 -   75 km->    NG;    Q1033;                                 Nigeria;190886311;   9.0;   8.0
✅        North Macedonia                        41.6,  21.7 -    5 km->    MK;     Q221;                         North Macedonia;  2075301;  41.6;  21.7
✅                 Norway                        60.5,   8.5 -    0 km->    NO;      Q20;                                  Norway;  5367580;  65.0;  11.0
✅                   Oman                        21.0,  57.0 -    0 km->    OM;     Q842;                                    Oman;  4636262;  21.0;  57.0
✅               Pakistan                        30.4,  69.3 -  165 km->    PK;     Q843;                                Pakistan;197015955;  30.0;  71.0
✅                 Panama                         8.5, -80.8 -   47 km->    PA;     Q804;                                  Panama;  4098587;   8.6; -80.4
✅       Papua New Guinea                        -6.3, 144.0 -  337 km->    PG;     Q691;                        Papua New Guinea;  8251162;  -6.3; 147.0
✅               Paraguay                       -23.4, -58.4 -   46 km->    PY;     Q733;                                Paraguay;  6802295; -23.5; -58.0
✅                   Peru                        -9.2, -75.0 -  111 km->    PE;     Q419;                                    Peru; 30375603;  -9.4; -76.0
✅            Philippines                        13.0, 122.0 -  155 km->    PH;     Q928;                             Philippines;100981437;  12.0; 123.0
✅                 Poland                        51.9,  19.1 -   13 km->    PL;      Q36;                                  Poland; 38454576;  52.0;  19.0
✅               Portugal                        39.4,  -8.2 -  114 km->    PT;      Q45;                                Portugal; 10600000;  38.7;  -9.2
✅                  Qatar                        25.4,  51.2 -   10 km->    QA;     Q846;                                   Qatar;  2639211;  25.3;  51.2
✅                Romania                        45.9,  25.0 -    7 km->    RO;     Q218;                                 Romania; 19586539;  46.0;  25.0
✅                 Russia                        60.0,  90.0 -  584 km->    RU;     Q159;                                  Russia;146804372;  62.0; 100.0
✅                 Rwanda                        -1.9,  29.9 -    0 km->    RW;    Q1037;                                  Rwanda; 12208407;  -1.9;  29.9
✅            Saint Lucia                        13.9, -61.0 -    4 km->    LC;     Q760;                             Saint Lucia;   178844;  13.9; -61.0
✅ Saint Vincent and the Grenadines                        13.0, -61.3 -   21 km->    VC;     Q757;        Saint Vincent and the Grenadines;   109373;  13.2; -61.2
✅             San Marino                        43.9,  12.5 -    1 km->    SM;     Q238;                              San Marino;    31595;  43.9;  12.5
✅           Saudi Arabia                        24.0,  45.0 -   95 km->    SA;     Q851;                            Saudi Arabia; 33000000;  23.7;  44.1
✅                Senegal                        14.5, -14.5 -   23 km->    SN;    Q1041;                                 Senegal; 14133280;  14.4; -14.3
✅                 Serbia                        44.0,  21.0 -    9 km->    RS;     Q403;                                  Serbia;  7022268;  44.0;  20.9
✅             Seychelles                        -4.7,  55.5 -  403 km->    SC;    Q1042;                              Seychelles;    95843;  -7.1;  52.8
✅              Singapore                         1.3, 103.8 -    4 km->    SG;     Q334;                               Singapore;  5888926;   1.3; 103.8
✅               Slovakia                        48.7,  19.7 -   43 km->    SK;     Q214;                                Slovakia;  5439892;  49.0;  20.0
✅               Slovenia                        46.2,  15.0 -   17 km->    SI;     Q215;                                Slovenia;  2066880;  46.0;  15.0
✅                Somalia                         5.2,  46.2 -  129 km->    SO;    Q1045;                                 Somalia; 11031386;   6.0;  47.0
✅           South Africa                       -30.6,  22.9 -  201 km->    ZA;     Q258;                            South Africa; 57725600; -29.0;  24.0
✅                  Spain                        40.0,  -4.0 -   85 km->    ES;      Q29;                                   Spain; 46528024;  40.0;  -3.0
✅              Sri Lanka                         7.0,  81.0 -    0 km->    LK;     Q854;                               Sri Lanka; 21444000;   7.0;  81.0
✅                  Sudan                        12.9,  30.2 -  305 km->    SD;    Q1049;                                   Sudan; 40533330;  15.0;  32.0
✅               Suriname                         3.9, -56.0 -    9 km->    SR;     Q730;                                Suriname;   539276;   4.0; -56.0
✅                 Sweden                        63.0,  16.0 -  229 km->    SE;      Q34;                                  Sweden; 10327589;  61.0;  15.0
✅            Switzerland                        46.8,   8.2 -    2 km->    CH;      Q39;                             Switzerland;  8211700;  46.8;   8.2
✅                Taiwan*                        23.7, 121.0 -    0 km-> CN-TW;   Q57251;Taiwan Province, People's Republic of China; 23140000;  23.7; 121.0
✅               Tanzania                        -6.4,  34.9 -    8 km->    TZ;     Q924;                                Tanzania; 57310019;  -6.3;  34.9
✅               Thailand                        15.0, 101.0 -  111 km->    TH;     Q869;                                Thailand; 65931550;  14.0; 101.0
✅                   Togo                         8.6,   0.8 -   57 km->    TG;     Q945;                                    Togo;  7797694;   8.2;   1.2
✅    Trinidad and Tobago                        10.7, -61.2 -   32 km->    TT;     Q754;                     Trinidad and Tobago;  1369125;  10.7; -61.5
✅                Tunisia                        34.0,   9.0 -   92 km->    TN;     Q948;                                 Tunisia; 11565204;  34.0;  10.0
✅                 Turkey                        39.0,  35.2 -   66 km->    TR;      Q43;                                  Turkey; 82003882;  39.0;  36.0
✅                 Uganda                         1.0,  32.0 -   53 km->    UG;    Q1036;                                  Uganda; 42862958;   1.3;  32.4
✅                Ukraine                        48.4,  31.2 -   92 km->    UA;     Q212;                                 Ukraine; 42558328;  49.0;  32.0
✅   United Arab Emirates                        24.0,  54.0 -   54 km->    AE;     Q878;                    United Arab Emirates;  9400145;  24.4;  54.3
✅         United Kingdom              Bermuda   32.3, -64.8 -    3 km->    BM;   Q23635;                                 Bermuda;    65024;  32.3; -64.8
✅         United Kingdom       Cayman Islands   19.3, -81.3 -   82 km->    KY;    Q5785;                          Cayman Islands;    58435;  19.5; -80.5
✅         United Kingdom      Channel Islands   49.4,  -2.4 -    7 km->     ?; Q3405693;                                    Sark;      600;  49.4;  -2.4
✅         United Kingdom            Gibraltar   36.1,  -5.4 -    1 km->    GI;    Q1410;                               Gibraltar;    33140;  36.1;  -5.3
✅         United Kingdom          Isle of Man   54.2,  -4.5 -    3 km->    IM;    Q9676;                             Isle of Man;    85888;  54.2;  -4.5
✅         United Kingdom           Montserrat   16.7, -62.2 -    2 km->    MS;   Q13353;                              Montserrat;     5215;  16.8; -62.2
✅         United Kingdom                        55.4,  -3.4 -    0 km->GB-UKM;     Q145;                          United Kingdom; 65102385;  54.6;  -2.0
✅                Uruguay                       -32.5, -55.8 -   86 km->    UY;      Q77;                                 Uruguay;  3456750; -32.7; -56.6
✅                     US                        37.1, -95.7 -    0 km->    US;      Q30;                United States of America;325145963;  38.9; -77.0
✅             Uzbekistan                        41.4,  64.6 -  126 km->    UZ;     Q265;                              Uzbekistan; 32387200;  41.0;  66.0
✅              Venezuela                         6.4, -66.6 -  180 km->    VE;     Q717;                               Venezuela; 28515829;   8.0; -67.0
✅                Vietnam                        16.0, 108.0 -    0 km->    VN;     Q881;                                 Vietnam; 94660000;  16.0; 108.0
✅                 Zambia                       -15.4,  28.3 -  160 km->    ZM;     Q953;                                  Zambia; 17094130; -14.0;  28.0
✅               Zimbabwe                       -20.0,  30.0 -  111 km->    ZW;     Q954;                                Zimbabwe; 16529904; -19.0;  30.0
✅               Dominica                        15.4, -61.4 -    4 km->    DM;     Q784;                                Dominica;    73925;  15.4; -61.3
✅                Grenada                        12.1, -61.7 -    1 km->    GD;     Q769;                                 Grenada;   107825;  12.1; -61.7
✅             Mozambique                       -18.7,  35.5 -   67 km->    MZ;    Q1029;                              Mozambique; 29668834; -19.0;  35.0
✅                  Syria                        34.8,  39.0 -   59 km->    SY;     Q858;                                   Syria; 18269868;  35.2;  38.6
✅            Timor-Leste                        -8.9, 125.7 -   11 km->    TL;     Q574;                              East Timor;  1296311;  -9.0; 125.8
✅                 Belize                        13.2, -59.5 -    3 km->    BB;     Q244;                                Barbados;   285719;  13.2; -59.6
✅                   Laos                        19.9, 102.5 -  242 km->    LA;     Q819;                                    Laos;  6858160;  18.2; 104.0
✅                  Libya                        26.3,  17.2 -   77 km->    LY;    Q1016;                                   Libya;  6678567;  27.0;  17.0
✅     West Bank and Gaza                        32.0,  35.2 -    0 km->    IL;     Q801;                                  Israel;  8891800;  31.0;  35.0
✅          Guinea-Bissau                        11.8, -15.2 -   29 km->    GW;    Q1007;                           Guinea-Bissau;  1861283;  12.0; -15.0
✅                   Mali                        17.6,  -4.0 -   63 km->    ML;     Q912;                                    Mali; 18541980;  17.0;  -4.0
✅  Saint Kitts and Nevis                        17.4, -62.8 -   13 km->    KN;     Q763;                   Saint Kitts and Nevis;    54191;  17.3; -62.7
✅                 Canada Northwest Territories   64.8,-124.8 -  301 km-> CA-NT;    Q2007;                   Northwest Territories;    44718;  66.0;-119.0
✅                 Canada                Yukon   64.3,-135.0 -  397 km-> CA-YT;    Q2009;                                   Yukon;    38669;  60.7;-135.1
✅                 Kosovo                        42.6,  20.9 -    0 km->    RS;     Q403;                                  Serbia;  7022268;  44.0;  20.9
✅                  Burma                        21.9,  96.0 -    0 km->    MM;     Q836;                                 Myanmar; 53370609;  22.0;  96.0
✅         United Kingdom             Anguilla   18.2, -63.1 -    2 km->    AI;   Q25228;                                Anguilla;    16086;  18.2; -63.0
✅         United Kingdom British Virgin Islands   18.4, -64.6 -   17 km->    VG;   Q25305;                  British Virgin Islands;    31758;  18.5; -64.5
✅         United Kingdom Turks and Caicos Islands   21.7, -71.8 -   23 km->    TC;   Q18221;                Turks and Caicos Islands;    33098;  21.8; -71.6
✅               Botswana                       -22.3,  24.7 -  103 km->    BW;     Q963;                                Botswana;  2291661; -22.2;  23.7
✅                Burundi                        -3.4,  29.9 -   34 km->    BI;     Q967;                                 Burundi; 10864245;  -3.7;  29.8
✅           Sierra Leone                         8.5, -11.8 -   16 km->    SL;    Q1044;                            Sierra Leone;  7557212;   8.5; -11.9
</pre>