import { SpiceProvider } from './spice-provider.js';

const provider = new SpiceProvider('homestead', 'API_KEY');

console.log('The latest block number is', await provider.getBlockNumber());
