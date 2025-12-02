import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/theme/controller/theme_controller.dart';
import '../modules/authentication/presentation/providers/auth_provider.dart';
import '../modules/onboarding/presentation/providers/onboarding_provider.dart';

// Helper function to create a ChangeNotifierProvider from a class type
ChangeNotifierProvider<T> _createProvider<T extends ChangeNotifier>(
  T Function() creator,
) {
  return ChangeNotifierProvider<T>(create: (_) => creator());
}

// Export a MultiProvider widget
Widget multiProvider({required Widget child}) {
  return MultiProvider(
    providers: [
      _createProvider(() => ThemeController()),
      _createProvider(() => AuthProvider()),
      _createProvider(() => OnboardingProvider(totalPages: 4)),
    ],
    child: child,
  );
}
