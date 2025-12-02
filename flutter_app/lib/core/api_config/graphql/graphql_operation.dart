import 'dart:developer';

import 'package:flutter_app/core/api_config/graphql/graphql_url_config.dart';
import 'package:graphql_flutter/graphql_flutter.dart';


class GraphQLOperation {
  static Future<QueryResult> executeOperation(
    String operationString,
    OperationType type, {
    Map<String, dynamic>? variables,
  }) async {
    final client = await GraphQLConfig.initializeClient();
    final gqlDoc = gql(operationString);
    final duration = Duration(seconds: apiCallTimeOut);

    late QueryResult result;

    if (type == OperationType.query) {
      final options = QueryOptions(
        document: gqlDoc,
        variables: variables ?? {},
        fetchPolicy: FetchPolicy.networkOnly,
        queryRequestTimeout: duration,
      );
      result = await client.query(options);
    } else {
      final options = MutationOptions(
        document: gqlDoc,
        variables: variables ?? {},
        queryRequestTimeout: duration,
      );
      result = await client.mutate(options);
    }

    if (result.hasException) {
      throw Exception(result.exception.toString());
    }

    return result;
  }

  static Future<QueryResult> performQuery(
    String query, {
    Map<String, dynamic>? variables,
  }) {
    return executeOperation(query, OperationType.query, variables: variables);
  }

  static Future<QueryResult> performMutation(
    String mutation, {
    Map<String, dynamic>? variables,
    bool isMrejeshoApiCall = false,
  }) {
    return executeOperation(
      mutation,
      OperationType.mutation,
      variables: variables,
    );
  }
}
