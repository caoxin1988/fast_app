cd /home/jsj423/fast_app

git pull

cur_date="log""`date +%Y%m%d-%H%M`"
file_name=$cur_date
echo $file_name

if [ ! -d "log" ]; then
    mkdir "log"
fi

cd log

if [ -f $file_name ]; then
    echo "is exist"
else
    echo "not exist"
    touch $file_name
fi

cd ..

/opt/anaconda3/bin/python fast_app.py --write_mongo=True --write_mysql=True --generate_file=True --days=3 >"log/"$file_name
