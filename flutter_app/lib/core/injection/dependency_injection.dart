import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:get_it/get_it.dart';

import '../../modules/authentication/data/services/auth_local_data_source.dart';
import '../../shared/utilities/helper_methods/device_security_checker.dart';
import '../api_config/graphql/graphql_service.dart';
import '../storage/flutter_secure_storage_service.dart';

final getIt = GetIt.instance;

void setup() {
  getIt.registerLazySingleton<FlutterSecureStorage>(
    () => const FlutterSecureStorage(),
  );
  getIt.registerLazySingleton<AuthSecureStorageDataSource>(
    () => AuthSecureStorageDataSourceImpl(getIt<FlutterSecureStorageService>()),
  );
  getIt.registerLazySingleton<FlutterSecureStorageService>(
    () => SecureStorageServiceImpl(getIt<FlutterSecureStorage>()),
  );
  getIt.registerLazySingleton<RestApiService>(() => RestApiService());
  getIt.registerLazySingleton<DeviceSecurityChecker>(
    () => DeviceSecurityChecker(),
  );

  getIt.registerLazySingleton<GraphQLService>(() => GraphQLService());
}
