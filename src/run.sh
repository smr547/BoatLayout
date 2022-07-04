

cp ~/Downloads/physical_structure_of_namadgi_3\ -\ Regions.csv ../data/namadgi_3_Regions.csv
cp ~/Downloads/physical_structure_of_namadgi_3\ -\ Spaces.csv ../data/namadgi_3_Spaces.csv
cp ~/Downloads/physical_structure_of_namadgi_3\ -\ Accesses.csv ../data/namadgi_3_Accesses.csv
./build_dot.py -s ../data/namadgi_3_Spaces.csv -a ../data/namadgi_3_Accesses.csv -r ../data/namadgi_3_Regions.csv -f 0,1,2,3,8 > namadgi3_upperDeck_companionway.dot
dot -Tpdf namadgi3_upperDeck_companionway.dot -o namadgi3_upperDeck_companionway.pdf
./build_dot.py -s ../data/namadgi_3_Spaces.csv -a ../data/namadgi_3_Accesses.csv -r ../data/namadgi_3_Regions.csv -f 4 > namadgi3_galley.dot
dot -Tpdf namadgi3_galley.dot -o namadgi3_galley.pdf
./build_dot.py -s ../data/namadgi_3_Spaces.csv -a ../data/namadgi_3_Accesses.csv -r ../data/namadgi_3_Regions.csv -f 5 > namadgi3_saloon.dot
dot -Tpdf namadgi3_saloon.dot -o namadgi3_saloon.pdf
./build_dot.py -s ../data/namadgi_3_Spaces.csv -a ../data/namadgi_3_Accesses.csv -r ../data/namadgi_3_Regions.csv -f 6 > namadgi3_fwd_accommodation.dot
dot -Tpdf namadgi3_fwd_accommodation.dot -o namadgi3_fwd_accommodation.pdf
./build_dot.py -s ../data/namadgi_3_Spaces.csv -a ../data/namadgi_3_Accesses.csv -r ../data/namadgi_3_Regions.csv -f 7 > namadgi3_aft_accommodation.dot
dot -Tpdf namadgi3_aft_accommodation.dot -o namadgi3_aft_accommodation.pdf
