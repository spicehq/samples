import { SpiceProvider } from './spice-provider.js';

const provider = new SpiceProvider();

console.log('The latest block number is', await provider.getBlockNumber());
