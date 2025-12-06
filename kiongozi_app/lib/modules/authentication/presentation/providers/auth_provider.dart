import 'dart:convert';
import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

import '../../../../core/injection/dependency_injection.dart';
import '../../data/services/auth_local_data_source.dart';
import '../../data/services/auth_remote_data_source.dart';

class AuthProvider extends ChangeNotifier {
  bool isLoading = false;
  bool isLoggedIn = false;
  String message = "";
  final dio = Dio();

  final authService = AuthRemoteDataSource();
  Future<void> login({
    required String username,
    required String password,
  }) async {
    isLoading = true;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      notifyListeners();
    });
    try {
      final response = await authService.userLoginService(
        username: username,
        password: password,
      );

      if (response.statusCode == 200) {
        final body = jsonDecode(response.body);

        final authLocalDataSource = getIt<AuthSecureStorageDataSource>();
        log("---------data--------------_${response.body.runtimeType}");

        log("-----------------------------${body['data']['portal']}");
        final formatedJsonData = body['data']['portal']
            .toString()
            .replaceAll('{', '{"')
            .replaceAll('}', '"}')
            .replaceAll(': ', '": "')
            .replaceAll(', ', '", "');

        await authLocalDataSource.saveAuthResponse(formatedJsonData);
        message = "Logged in successfully!";
      } else if (response.statusCode == 400) {
        message = "Incorrect Credentials!";
      } else {
        message = "Incorrect Credentials!";
      }
    } catch (e, trace) {
      log("---------datadffsd--------------_$e");
      log("---------datadffsd--------------_$trace");
      message = "Internal server error occurred";
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }
}
