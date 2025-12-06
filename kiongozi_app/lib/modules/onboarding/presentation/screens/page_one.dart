import 'package:flutter/material.dart';

import '../../../../core/constants/dimensions.dart';
import '../../../../core/theme/app_colors.dart' show AppColors;
import '../widgets/onboarding_top_component.dart';

class PageOne extends StatefulWidget {
  final PageController pageController;
  const PageOne({super.key, required this.pageController});

  @override
  State<PageOne> createState() => _PageOneState();
}

class _PageOneState extends State<PageOne> {
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
                  'https://via.placeholder.com/300x200.png?text=Time+Management', // Placeholder network image
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
                  "Welcome to Kiongozi", // Replaced localization.welcomeTitle with hardcoded string
                  style: theme.textTheme.titleLarge!.copyWith(
                    fontWeight: FontWeight.w900,
                    color: AppColors.tealGreen,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    "Manage your time and tasks efficiently with our app.", // Replaced localization.welcomePage1Desc with hardcoded string
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
