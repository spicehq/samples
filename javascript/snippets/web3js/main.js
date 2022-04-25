import Web3 from 'web3';

const web3 = new Web3('https://data.spiceai.io/eth');
console.log('The latest block number is', await web3.eth.getBlockNumber());
