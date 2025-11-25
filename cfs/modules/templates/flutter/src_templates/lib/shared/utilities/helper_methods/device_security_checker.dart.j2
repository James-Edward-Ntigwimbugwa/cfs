import 'package:device_safety_info/device_safety_info.dart';

class DeviceSecurityChecker {
  Future<SecurityCheckResult> checkDeviceSecurity() async {
    try {
      final isJailBroken = await DeviceSafetyInfo.isRootedDevice;
      final isRealDevice = await DeviceSafetyInfo.isRealDevice;
      final isMockLocation = await DeviceSafetyInfo.isVPNCheck;
      final isOnExternalStorage = await DeviceSafetyInfo.isExternalStorage;
      final isDevelopmentMode = await DeviceSafetyInfo.isDeveloperMode;

      if (isJailBroken) {
        return SecurityCheckResult.failure("Device is jailbroken or rooted.");
      }
      if (!isRealDevice) {
        return SecurityCheckResult.failure(
            "Device is an emulator or simulator.");
      }
      if (isMockLocation) {
        return SecurityCheckResult.failure("Mock location is enabled.");
      }
      if (isOnExternalStorage) {
        return SecurityCheckResult.failure(
            "App is installed on external storage.");
      }
      if (isDevelopmentMode) {
        return SecurityCheckResult.failure("Developer mode is enabled.");
      }

      return SecurityCheckResult.success();
    } catch (e) {
      return SecurityCheckResult.failure('Error checking device: $e');
    }
  }
}

class SecurityCheckResult {
  final bool isSecure;
  final String? message;

  SecurityCheckResult._({required this.isSecure, this.message});

  factory SecurityCheckResult.success() =>
      SecurityCheckResult._(isSecure: true);
  factory SecurityCheckResult.failure(String message) =>
      SecurityCheckResult._(isSecure: false, message: message);
}
