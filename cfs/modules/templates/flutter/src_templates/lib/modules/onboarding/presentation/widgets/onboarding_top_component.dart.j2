import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/constants/dimensions.dart';
import '../../../../core/theme/app_colors.dart';
import '../providers/on_boarding_provider.dart';

class OnboardingTopComponent extends StatelessWidget {
  final PageController controller;
  const OnboardingTopComponent({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Consumer<OnboardingProvider>(
      builder: (context, provider, child) {
        return Padding(
          padding: EdgeInsets.symmetric(
            horizontal: Dimensions.width8,
            vertical: 8,
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              // Logo
              Row(
                spacing: 4,
                children: [
                  Image.network(
                    'https://via.placeholder.com/50x50.png?text=Kiongozi', // Placeholder network image
                    height: 20,
                    loadingBuilder: (context, child, loadingProgress) {
                      if (loadingProgress == null) return child;
                      return SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2));
                    },
                    errorBuilder: (context, error, stackTrace) {
                      return Icon(Icons.error, size: 20, color: AppColors.greenMain);
                    },
                  ),
                  Text(
                    "Kiongozi ",
                    style: theme.textTheme.titleMedium!.copyWith(
                      color: AppColors.greenMain,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  Text(
                    "App",
                    style: theme.textTheme.titleMedium!.copyWith(
                      color: AppColors.black,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                ],
              ),

              // Skip button (hide on last page)
              if (provider.currentPage != provider.totalPages - 1) ...[
                GestureDetector(
                  onTap: () {
                    provider.skipToLastPage(controller);
                  },
                  child: Text(
                    "Skip",
                    style: theme.textTheme.bodyMedium!.copyWith(
                      color: AppColors.greenMain,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ],
          ),
        );
      },
    );
  }
}