import 'dart:convert';

import 'package:http/http.dart' as http;

import '../../../modules/authentication/data/services/auth_local_data_source.dart';
import '../../injection/dependency_injection.dart';
import '../api_parameters.dart';

class RestApiService {
  final authLocalDataSource = getIt<AuthSecureStorageDataSource>();

  static final RestApiService _instance = RestApiService._internal();
  factory RestApiService() => _instance;
  RestApiService._internal();

  Future<Map<String, String>> _buildHeaders({bool requiresAuth = false}) async {
    final headers = {'Content-Type': 'application/json'};
    if (requiresAuth) {
      final token = await authLocalDataSource.getToken();
      final type = await authLocalDataSource.getTokenType();

      if (token != null && token.isNotEmpty) {
        headers['Authorization'] = '$type $token';
      }
    }
    return headers;
  }

  Future<http.Response> get(String endpoint, {bool requireAuth = false}) async {
    final headers = await _buildHeaders(requiresAuth: requireAuth);
    return http
        .get(Uri.parse('$baseUrl/$endpoint'), headers: headers)
        .timeout(Duration(seconds: apiCallTimeOut));
  }

  Future<http.Response> post(
    String endpoint,
    dynamic data, {
    bool requireAuth = false,
    Map<String, String>? headers,
  }) async {
    final effectiveHeaders =
        headers ?? await _buildHeaders(requiresAuth: requireAuth);

    dynamic bodyToSend;

    final contentType = effectiveHeaders['Content-Type'];

    if (contentType == 'application/x-www-form-urlencoded') {
      bodyToSend = data.entries
          .map(
            (e) =>
                '${Uri.encodeComponent(e.key)}=${Uri.encodeComponent(e.value.toString())}',
          )
          .join('&');
    } else {
      bodyToSend = jsonEncode(data);
    }

    return http
        .post(
          Uri.parse('$baseUrl/$endpoint'),
          headers: effectiveHeaders,
          body: bodyToSend,
        )
        .timeout(Duration(seconds: apiCallTimeOut));
  }

  Future<http.Response> put(
    String endpoint,
    dynamic data, {
    bool requireAuth = false,
  }) async {
    final headers = await _buildHeaders(requiresAuth: requireAuth);
    return http
        .put(
          Uri.parse('$baseUrl/$endpoint'),
          headers: headers,
          body: jsonEncode(data),
        )
        .timeout(Duration(seconds: apiCallTimeOut));
  }

  Future<http.Response> delete(
    String endpoint, {
    bool requireAuth = false,
  }) async {
    final headers = await _buildHeaders(requiresAuth: requireAuth);
    return http.delete(Uri.parse('$baseUrl/$endpoint'), headers: headers);
  }
}
