import type { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  DateTime: { input: any; output: any; }
};

export type AiInterpretation = {
  __typename?: 'AIInterpretation';
  content: Scalars['String']['output'];
  context: Scalars['String']['output'];
  generatedAt: Scalars['DateTime']['output'];
  id: Scalars['String']['output'];
};

export type Artist = {
  __typename?: 'Artist';
  bio: Scalars['String']['output'];
  id: Scalars['String']['output'];
  name: Scalars['String']['output'];
};

export type Artwork = {
  __typename?: 'Artwork';
  artist: Artist;
  id: Scalars['String']['output'];
  imageUrl: Scalars['String']['output'];
  title: Scalars['String']['output'];
};

export type Collection = {
  __typename?: 'Collection';
  artworks: Array<Artwork>;
  description?: Maybe<Scalars['String']['output']>;
  id: Scalars['String']['output'];
  title: Scalars['String']['output'];
};

export type Query = {
  __typename?: 'Query';
  artist?: Maybe<Artist>;
  artwork?: Maybe<Artwork>;
  collection?: Maybe<Collection>;
  collections: Array<Collection>;
  generateArtworkInterpretation?: Maybe<AiInterpretation>;
};


export type QueryArtworkArgs = {
  id: Scalars['String']['input'];
};


export type QueryCollectionArgs = {
  id: Scalars['String']['input'];
};


export type QueryGenerateArtworkInterpretationArgs = {
  artworkId: Scalars['String']['input'];
};

export type GetArtistQueryVariables = Exact<{ [key: string]: never; }>;


export type GetArtistQuery = { __typename?: 'Query', artist?: { __typename?: 'Artist', id: string, name: string, bio: string } | null };

export type GenerateArtworkInterpretationQueryVariables = Exact<{
  artworkId: Scalars['String']['input'];
}>;


export type GenerateArtworkInterpretationQuery = { __typename?: 'Query', generateArtworkInterpretation?: { __typename?: 'AIInterpretation', id: string, content: string, generatedAt: any, context: string } | null };

export type GetCollectionsQueryVariables = Exact<{ [key: string]: never; }>;


export type GetCollectionsQuery = { __typename?: 'Query', collections: Array<{ __typename?: 'Collection', id: string, title: string, description?: string | null, artworks: Array<{ __typename?: 'Artwork', id: string, title: string, imageUrl: string, artist: { __typename?: 'Artist', id: string, name: string } }> }> };


export const GetArtistDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetArtist"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"artist"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"bio"}}]}}]}}]} as unknown as DocumentNode<GetArtistQuery, GetArtistQueryVariables>;
export const GenerateArtworkInterpretationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GenerateArtworkInterpretation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"artworkId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"generateArtworkInterpretation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"artworkId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"artworkId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"content"}},{"kind":"Field","name":{"kind":"Name","value":"generatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"context"}}]}}]}}]} as unknown as DocumentNode<GenerateArtworkInterpretationQuery, GenerateArtworkInterpretationQueryVariables>;
export const GetCollectionsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetCollections"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"collections"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"artworks"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"imageUrl"}},{"kind":"Field","name":{"kind":"Name","value":"artist"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetCollectionsQuery, GetCollectionsQueryVariables>;