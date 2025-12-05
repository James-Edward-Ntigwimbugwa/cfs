import 'dart:convert';
import 'dart:developer';

import '../../../../core/storage/flutter_secure_storage_keys.dart';
import '../../../../core/storage/flutter_secure_storage_service.dart';

abstract class AuthSecureStorageDataSource {
  Future<void> saveAuthResponse(String authResponse);
  Future<void> saveItem({required String key, required String value});
  Future<String?> getItem({required String key});
  Future<String?> getToken();
  Future<String?> getTokenType();
  Future<String?> getRefreshToken();
  Future<String?> getTokenExpireTime();
  Future<Map<String, dynamic>?> getUserInfo();
  Future<void> deleteToken();
}

class AuthSecureStorageDataSourceImpl implements AuthSecureStorageDataSource {
  final FlutterSecureStorageService flutterSecureStorageService;

  AuthSecureStorageDataSourceImpl(this.flutterSecureStorageService);

  @override
  Future<void> saveAuthResponse(String authResponse) async {
    await flutterSecureStorageService.saveItem(
      key: FlutterSecureStorageKeys.authResponse,
      value: authResponse,
    );
  }

  @override
  Future<void> saveItem({required String key, required String value}) async {
    await flutterSecureStorageService.saveItem(key: key, value: value);
  }

  @override
  Future<String?> getItem({required String key}) async {
    final response = await flutterSecureStorageService.getItem(key: key);
    return response;
  }

  @override
  Future<String?> getToken() async {
    final authResponse = await flutterSecureStorageService.getItem(
      key: FlutterSecureStorageKeys.authResponse,
    );
    if (authResponse != null) {
      final authData = jsonDecode(authResponse);
      return authData['token'];
    }
    return null;
  }

  @override
  Future<String?> getTokenExpireTime() async {
    final authResponse = await flutterSecureStorageService.getItem(
      key: FlutterSecureStorageKeys.authResponse,
    );
    if (authResponse != null) {
      final authData = jsonDecode(authResponse);
      return authData['tokenExpiresAt'];
    }
    return null;
  }

  @override
  Future<String> getTokenType() async {
    final authResponse = await flutterSecureStorageService.getItem(
      key: FlutterSecureStorageKeys.authResponse,
    );
    if (authResponse != null) {
      final authData = jsonDecode(authResponse);
      log("--------dads---------$authResponse");
      return authData['tokenType'];
    }
    return 'Bearer';
  }

  @override
  Future<String> getRefreshToken() async {
    final authResponse = await flutterSecureStorageService.getItem(
      key: FlutterSecureStorageKeys.authResponse,
    );
    if (authResponse != null) {
      final authData = jsonDecode(authResponse);
      return authData['refreshToken'];
    }
    return 'Bearer';
  }

  @override
  Future<Map<String, dynamic>?> getUserInfo() async {
    final authResponse = await flutterSecureStorageService.getItem(
      key: FlutterSecureStorageKeys.authResponse,
    );
    if (authResponse != null) {
      final authData = jsonDecode(authResponse);
      return {
        'username': authData['username'],
        'userUid': authData['userUid'],
        'userId': authData['userId'],
      };
    }
    return null;
  }

  @override
  Future<void> deleteToken() async {
    await flutterSecureStorageService.deleteItem(
      key: FlutterSecureStorageKeys.authResponse,
    );
  }
}
