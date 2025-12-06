import 'package:flutter/material.dart';

/// Provides easy access to frequently used theme and media values.
/// Safe to use inside any [StatefulWidget].
mixin AppThemeMixin<T extends StatefulWidget> on State<T> {
  ColorScheme get colorScheme => Theme.of(context).colorScheme;
  TextTheme get textTheme => Theme.of(context).textTheme;
  double get topPadding => MediaQuery.paddingOf(context).top;
}
