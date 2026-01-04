import { GraphQLClient } from 'graphql-request';

const API_URL = import.meta.env.VITE_API_URL;

if (!API_URL) {
  throw new Error(
    'VITE_API_URL environment variable is not defined. Please check your .env.local file.'
  );
}

export const graphqlClient = new GraphQLClient(API_URL, {
  headers: {
    'Content-Type': 'application/json',
  },
});
