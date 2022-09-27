'use strict';

import {
  UrlJsonRpcProvider,
  showThrottleMessage,
} from '@ethersproject/providers';

import { Logger } from '@ethersproject/logger';
const logger = new Logger('providers/5.5.1');

const defaultApiKey = '3439|6806e8faf10643e2bde903920bbcb1ff';

export class SpiceProvider extends UrlJsonRpcProvider {
  static getApiKey(apiKey) {
    if (apiKey == null) {
      return defaultApiKey;
    }
    if (apiKey && typeof apiKey !== 'string') {
      logger.throwArgumentError('invalid apiKey', 'apiKey', apiKey);
    }
    return apiKey;
  }

  static getUrl(network, apiKey) {
    const host = 'https://data.spiceai.io';
    let path = null;
    switch (network.name) {
      case 'homestead':
        path = '/eth';
        break;
      case 'polygon':
        path = '/polygon';
        break;
      default:
        logger.throwArgumentError(
          'unsupported network',
          'network',
          arguments[0]
        );
    }

    return {
      allowGzip: true,
      url: host + path,
      throttleCallback: (attempt, url) => {
        if (apiKey === defaultApiKey) {
          showThrottleMessage();
        }
        return Promise.resolve(true);
      },
    };
  }

  isCommunityResource() {
    return this.apiKey === defaultApiKey;
  }
}
