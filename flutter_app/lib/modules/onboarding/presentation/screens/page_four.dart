import 'package:flutter/material.dart';

import '../../../../core/constants/dimensions.dart';
import '../../../../core/mixins/app_localization_mixin.dart';
import '../../../../core/theme/modes/app_colors.dart';
import '../../../../gen/assets.gen.dart';
import '../widgets/onboarding_top_component.dart';

class PageFour extends StatefulWidget {
  final PageController pageController;
  const PageFour({super.key, required this.pageController});

  @override
  State<PageFour> createState() => _PageFourState();
}

class _PageFourState extends State<PageFour> with LocalizationMixin {
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
                Assets.svg.newdesign.svg(height: Dimensions.screenWidth * .65),
                SizedBox(height: Dimensions.height8),
                Text(
                  localization.directives,
                  style: theme.textTheme.titleLarge!.copyWith(
                    fontWeight: FontWeight.w900,
                    color: AppColors.tealGreen,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    localization.directiveDescription,
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
