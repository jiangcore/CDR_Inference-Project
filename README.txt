echo " prepare datasets:  test.txt "
python prepare.py 
 
echo "start training.. to get model "
python main.py --config demo.train.config

 
echo "start decode... to  get rawout "
python main.py --config demo.decode.config
 
echo "process rawout  to get result.txt"
python  reassemble.py

 
echo " evaluate the result" 
./eval_mention.sh PubTator CDR_TestSet.PubTator.txt result.txt