import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/constants/dimensions.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../shared/widgets/custom_button.dart';
import '../../../../shared/widgets/text_component.dart';
import '../../../authentication/routes/authentication_paths.dart';

class NewOnboarding extends StatefulWidget {
  const NewOnboarding({super.key});

  @override
  State<NewOnboarding> createState() => _NewOnboardingState();
}

class _NewOnboardingState extends State<NewOnboarding> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                // Top: hii inafanya rangi kama iwe ina grow
                Color.lerp(
                  AppColors.greenMain.withAlpha(150),
                  AppColors.greenMain,
                  2,
                )!,
                // Bottom: whitish → gradually to tealGreen (kama top)
                Color.lerp(
                  Colors.white, // start color bottom
                  AppColors.tealGreen, // end color bottom
                  1, // tween progress
                )!,
              ],
            ),
          ),
          padding: EdgeInsets.symmetric(vertical: 10, horizontal: 16),
          child: Column(
            children: [
              SizedBox(height: Dimensions.height128),
              Center(
                child: Image.network(
                  'https://via.placeholder.com/300x200.png?text=Kiongozi+App', // Placeholder network image
                  scale: 1,
                  loadingBuilder: (context, child, loadingProgress) {
                    if (loadingProgress == null) return child;
                    return Center(child: CircularProgressIndicator());
                  },
                  errorBuilder: (context, error, stackTrace) {
                    return Icon(Icons.error, size: 100, color: Colors.white);
                  },
                ),
              ),
              SizedBox(height: Dimensions.height28),
              Align(
                alignment: Alignment.center,
                child:
                    TextComponent(
                      text: "Welcome to Kiongozi App",
                      fontWeight: FontWeight.w800,
                      fontSize: 28,
                      textAlignemt: TextAlign.center,
                    )
              ),
              SizedBox(height: Dimensions.height12),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: TextComponent(
                  text:
                      "Set, Plan, Track and Monitor directives, meetings, and progress all in one secure platform and achieve more.",
                  textAlignemt: TextAlign.center,
                  fontSize: 16,
                  fontWeight: FontWeight.w300,
                ),
              ),
              SizedBox(height: Dimensions.height20),
              SizedBox(
                width: double.infinity,
                height: Dimensions.height48,
                child: CustomButton(
                  onPressed: () {
                    context.push(AuthenticationPaths.login);
                  },
                  backgroundColor: AppColors.white,
                  padding: EdgeInsets.all(1),
                  borderRadius: 30,
                  child: TextComponent(
                    text: "Get Started",
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    textColor: AppColors.greenMain,
                  ),
                ),
              ),
              SizedBox(height: Dimensions.height40),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: TextComponent(
                  text: "Empowering productivity and accountability.",
                  textAlignemt: TextAlign.center,
                  fontSize: 14,
                  fontWeight: FontWeight.w200,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}