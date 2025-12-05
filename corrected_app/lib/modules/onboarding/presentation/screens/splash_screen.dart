import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:toastification/toastification.dart';

import '../../../../core/injection/dependency_injection.dart';
import '../../../../core/storage/flutter_secure_storage_keys.dart';
import '../../../../core/storage/flutter_secure_storage_service.dart';
import '../../../../core/theme/app_colors.dart';
import '../../routes/onboarding_paths.dart';

class SplashScreen extends StatefulWidget {
  /// If [blockInsecureDevice] is true, the app will show a toast message
  /// warning the user and exit instead of navigating to the next page.
  final bool blockInsecureDevice;

  const SplashScreen({super.key, this.blockInsecureDevice = false});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    navigateToNextPage();
  }

  Future<void> navigateToNextPage() async {
    final secureStorage = getIt<FlutterSecureStorageService>();
    String isFirstTimeLaunch =
        await secureStorage.getItem(
          key: FlutterSecureStorageKeys.isFirstAppLaunch,
        ) ??
        "yes";

    // If blockInsecureDevice is true → show toast and quit app
    if (widget.blockInsecureDevice) {
      Future.delayed(const Duration(seconds: 1), () {
        toastification.show(
          context: context,
          title: const Text("Security Warning"),
          description: const Text(
            "App can’t run on rooted devices, emulators, or with developer options enabled.\n"
            "Please use a physical device without root privileges and dev options off.",
          ),
          type: ToastificationType.error,
          style: ToastificationStyle.fillColored,
          autoCloseDuration: const Duration(seconds: 5),
          alignment: Alignment.bottomCenter,
          showProgressBar: true,
        );
      });

      // 👇 Close the app after 3 seconds
      Future.delayed(const Duration(seconds: 6), () {
        exit(0);
      });
      return;
    }

    // Otherwise, proceed normally
    Future.delayed(const Duration(seconds: 4), () {
      if (!context.mounted) return;

      if (isFirstTimeLaunch == "yes") {
        context.go(OnboardingPaths.onBoardingScreen);
      } else {
        // context.go(HomePaths.home);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: TweenAnimationBuilder<double>(
        tween: Tween(begin: 0.0, end: 1.0),
        duration: const Duration(seconds: 3),
        builder: (context, value, child) {
          return Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Color.lerp(
                    AppColors.greenMain.withAlpha(150),
                    AppColors.greenMain,
                    value,
                  )!,
                  Color.lerp(Colors.white, AppColors.tealGreen, value)!,
                ],
              ),
            ),
            child: child,
          );
        },
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          spacing: 16,
          children: [
            Center(
              child: Image.network(
                'https://via.placeholder.com/300x200.png?text=Kiongozi+App', // Placeholder network image
                scale: 12,
                loadingBuilder: (context, child, loadingProgress) {
                  if (loadingProgress == null) return child;
                  return Center(child: CircularProgressIndicator());
                },
                errorBuilder: (context, error, stackTrace) {
                  return Icon(Icons.error, size: 100, color: Colors.white);
                },
              ).animate().scale(duration: const Duration(seconds: 3)),
            ),
            Align(
              alignment: Alignment.center,
              child:
                  Text(
                    "KIONGOZI APP",
                    style: Theme.of(context).textTheme.titleLarge!.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                    ),
                  ).animate().fadeIn(
                    delay: const Duration(seconds: 3),
                    duration: const Duration(seconds: 1),
                  ),
            ),
          ],
        ),
      ),
    );
  }
}
