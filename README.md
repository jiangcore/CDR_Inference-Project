# CDR_Inference-Project
### This project is to build a module to inference diseases. 
### Input: CDR_Data
### Output: inference result of CDR_TestSet

Use PubTator Format to train model, and inference. There are 5 steps, including pre-process data, train module, decode data, generate result with module and evaluate.
Environment: Python: 2.7
Pytorch: 1.0.1 
OSX : 10.1 NCRF++

1) Preprocess CDR data

echo " prepare datasets:  test.txt "
python prepare.py 
 
2) Train Module in NCRF++
Configed NCRF++ to train without GPU, Configure file: "dh.train.config"
Output module file: "lstmcrf.6.model"

echo "start training.. to get model "
python main.py --config demo.train.config

3) Decode data in NCRF++
Configed NCRF++ to train without GPU, Configure file: "dh.decode.config" Output file: "raw.out"

echo "start decode... to  get rawout "
python main.py --config demo.decode.config
 
 
 4) Generate result
generate result via "assemble.py"

echo "process rawout  to get result.txt"
python  reassemble.py

 
5) Evaluation
Evaluated via bc5cdr_eval.jar

echo " evaluate the result" 
./eval_mention.sh PubTator CDR_TestSet.PubTator.txt result.txt
