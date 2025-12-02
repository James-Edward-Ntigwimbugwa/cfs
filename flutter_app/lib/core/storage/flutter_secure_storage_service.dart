import 'package:flutter_secure_storage/flutter_secure_storage.dart';

abstract class FlutterSecureStorageService {
  Future<void> saveItem({required String key, required String value});
  Future<String?> getItem({required String key});
  Future<void> deleteItem({required String key});
  Future<void> flushStorage();
}

class SecureStorageServiceImpl implements FlutterSecureStorageService {
  final FlutterSecureStorage _storage;

  SecureStorageServiceImpl(this._storage);

  // Method kwaajili ya kusave data locally
  @override
  Future<void> saveItem({required String key, required String value}) async {
    await _storage.write(key: key, value: value);
  }

  // Method kwaajili ya kuvuta data locally
  @override
  Future<String?> getItem({required String key}) async {
    return await _storage.read(key: key);
  }

  // Method kwaajili ya kufuta data specific locally
  @override
  Future<void> deleteItem({required String key}) async {
    await _storage.delete(key: key);
  }

  // Method kwaajili ya kufuta data zote locally, tumia hii only when
  // needed as user custom settings might be cleared too
  @override
  Future<void> flushStorage() async {
    await _storage.deleteAll();
  }
}
