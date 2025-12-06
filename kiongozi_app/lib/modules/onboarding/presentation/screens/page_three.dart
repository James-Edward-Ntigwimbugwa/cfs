import 'package:flutter/material.dart';

import '../../../../core/constants/dimensions.dart';
import '../../../../core/theme/app_colors.dart';
import '../widgets/onboarding_top_component.dart';

class PageThree extends StatefulWidget {
  final PageController pageController;
  const PageThree({super.key, required this.pageController});

  @override
  State<PageThree> createState() => _PageThreeState();
}

class _PageThreeState extends State<PageThree> {
  @override
  Widget build(BuildContext context) {
    final topPadding = MediaQuery.paddingOf(context).top;
    final theme = Theme.of(context);
    return Padding(
      padding: EdgeInsets.only(top: topPadding),
      child: Column(
        children: [
          OnboardingTopComponent(controller: widget.pageController),
          Expanded(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              spacing: Dimensions.height8,
              children: [
                Image.network(
                  'https://via.placeholder.com/300x200.png?text=Schedule+Management', // Placeholder network image
                  height: Dimensions.screenWidth * .65,
                  loadingBuilder: (context, child, loadingProgress) {
                    if (loadingProgress == null) return child;
                    return Center(child: CircularProgressIndicator());
                  },
                  errorBuilder: (context, error, stackTrace) {
                    return Icon(Icons.error, size: 100, color: Colors.white);
                  },
                ),
                SizedBox(height: Dimensions.height8),
                Text(
                  "Schedule Management", // Replaced localization.scheduleManagement with hardcoded string
                  style: theme.textTheme.titleLarge!.copyWith(
                    fontWeight: FontWeight.w900,
                    color: AppColors.tealGreen,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    "Organize your schedules and meetings seamlessly.", // Replaced localization.scheduleDescription with hardcoded string
                    textAlign: TextAlign.center,
                    style: theme.textTheme.bodyLarge!.copyWith(
                      color: theme.colorScheme.tertiary,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
