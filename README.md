# Federated Learning in Blockchain :
# How to run this Project:
Copy this command in your terminal
  ```
  git clone https://github.com/rag-hav/federated-blockchain
  ```
  Install requirements for this projects
  ```
  python -m pip install -r requirements.txt
  ```
  Install Solidity compiler
  ```
  python
    >>>import solcx
    >>>solcx.install_solc()
  ```
  go to blockcahin directory
  ```
  cd blockchain
  ```
  Make Node 1 with **Empty Password**
  ```
  ./makeNode.sh 1   
  ```
  start Node 1
  ```
  ./start.sh 1  
    >miner.start(1)
  ```
  Go back to previous directory
  ```
  cd ..
  ```
  Deploy Contract 
  ```
  python deploy.py 1
  ```
  Run Blockchain
  ```
  python main.py 1
  ```
  It should look something like this....
  ![image](https://user-images.githubusercontent.com/76650437/232193812-1619c283-bd26-407e-bda8-72cb01444db9.png)
  Run Frontend to monitor scores and accuracy
  ```
  cd app
  ./setup.sh 1 
  npm install
  npm run start
  ```
