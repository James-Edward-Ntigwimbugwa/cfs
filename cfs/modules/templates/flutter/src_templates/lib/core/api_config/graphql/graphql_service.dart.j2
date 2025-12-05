
import '../../enums/graphql_operation_enum.dart';
import 'graphql_operation.dart';

class GraphQLService {
  Future<T?> performGraphQLOperation<T>({
    required String operationString,
    required OperationType operationType,
    Map<String, dynamic>? variables,
    required T Function(Map<String, dynamic>) fromJson,
    String? responseKey,
    bool wrapInDataKey = false,
  }) async {
    try {
      final result = await GraphQLOperation.executeOperation(
        operationString,
        operationType,
        variables: variables,
      );

      if (result.hasException) {
        throw Exception("GraphQL error: ${result.exception.toString()}");
      }

      final data = result.data;
      if (data == null) return null;

      dynamic extractNestedData(Map<String, dynamic> data, String keyPath) {
        return keyPath.split('.').fold<dynamic>(data, (current, key) {
          if (current is Map<String, dynamic>) return current[key];
          return null;
        });
      }

      final rawData = responseKey != null
          ? extractNestedData(data, responseKey)
          : data;
      if (rawData == null) return null;

      if (wrapInDataKey && responseKey == null) {
        throw Exception("wrapInDataKey=true requires a responseKey");
      }

      final json = wrapInDataKey
          ? {
              'data': {responseKey!: rawData},
            }
          : rawData;

      return fromJson(json as Map<String, dynamic>);
    } catch (e) {
      throw Exception("Internal error: $e");
    }
  }
}
