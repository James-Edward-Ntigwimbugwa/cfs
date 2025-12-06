import 'package:http/http.dart';
import '../../../../core/api_config/rest/rest_api_service.dart';

class AuthRemoteDataSource {
  final apiService = RestApiService();

  //
  Future<Response> userLoginService({
    required String username,
    required String password,
  }) async {
    final response = await apiService.post(
      "auth/login",
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      {'username': username, 'password': password},
    );
    return response;
  }
}
