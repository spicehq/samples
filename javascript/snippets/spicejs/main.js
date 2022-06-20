/* npm install @spiceai/spice --save
 * or
 * yarn add @spiceai/spice
 */
import { SpiceClient } from '@spiceai/spice';

const spiceClient = new SpiceClient('API_KEY');
const arrowTable = await spiceClient.query(
  'SELECT number,hash FROM eth.recent_blocks ORDER BY number DESC LIMIT 10;'
);
console.log(arrowTable.toJSON());
