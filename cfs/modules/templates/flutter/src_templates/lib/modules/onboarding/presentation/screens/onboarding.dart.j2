import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:heroicons/heroicons.dart';
import 'package:provider/provider.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

import '../../../../core/constants/dimensions.dart';
import '../../../../core/injection/dependency_injection.dart';
import '../../../../core/storage/flutter_secure_storage_keys.dart';
import '../../../../core/storage/flutter_secure_storage_service.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../shared/widgets/custom_button.dart';
import '../../../../shared/widgets/glass_container.dart';
import '../../../authentication/routes/authentication_paths.dart';
import '../providers/on_boarding_provider.dart' show OnboardingProvider;
import 'page_four.dart';
import 'page_one.dart';
import 'page_three.dart';
import 'page_two.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  static final PageController _pageController = PageController();
  final List<Widget> pages = [
    PageOne(pageController: _pageController),
    PageTwo(pageController: _pageController),
    PageThree(pageController: _pageController),
    PageFour(pageController: _pageController),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<OnboardingProvider>(
      builder: (context, onBoardingProvider, child) {
        return Scaffold(
          backgroundColor: AppColors.white,
          body: Stack(
            children: [
              // Pages
              Positioned.fill(
                child: GlassContainer(
                  height: Dimensions.screenHeight,
                  child: PageView(
                    controller: _pageController,
                    children: pages,
                    onPageChanged: (index) {
                      onBoardingProvider.setPage(index);
                    },
                  ),
                ),
              ),

              // Indicator + Button
              Positioned(
                bottom: 40,
                left: 0,
                right: 0,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    SmoothPageIndicator(
                      controller: _pageController,
                      count: pages.length,
                      effect: ExpandingDotsEffect(
                        dotHeight: 5,
                        dotWidth: 20,
                        activeDotColor: AppColors.tealGreen,
                        dotColor: Colors.grey.shade300,
                      ),
                    ),
                    SizedBox(height: Dimensions.height16),
                    onBoardingProvider.currentPage == pages.length - 1
                        ? CustomButton(
                            borderRadius: 30,
                            padding: EdgeInsets.symmetric(
                              horizontal: Dimensions.width56,
                            ),
                            onPressed: () async {
                              final secureStorage =
                                  getIt<FlutterSecureStorageService>();
                              await secureStorage.saveItem(
                                key: FlutterSecureStorageKeys.isFirstAppLaunch,
                                value: "no",
                              );
                              context.go(AuthenticationPaths.login);
                            },
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text("Get Started"),
                                const SizedBox(width: 12),
                                // Animated arrows
                                Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: List.generate(3, (index) {
                                    return Padding(
                                      padding: const EdgeInsets.symmetric(
                                        horizontal: 2.0,
                                      ),
                                      child:
                                          HeroIcon(
                                                HeroIcons.chevronRight,
                                                size: 20,
                                                color: Colors.white,
                                              )
                                              .animate(
                                                onPlay: (controller) =>
                                                    controller.repeat(),
                                              )
                                              .fadeIn(
                                                delay: Duration(
                                                  milliseconds: 100 * index,
                                                ),
                                              )
                                              .then()
                                              .moveX(
                                                begin: 0,
                                                end: 8,
                                                duration: 500.ms,
                                              )
                                              .then()
                                              .moveX(
                                                begin: 8,
                                                end: 0,
                                                duration: 500.ms,
                                              ),
                                    );
                                  }),
                                ),
                              ],
                            ),
                          )
                        : CustomButton(
                            onPressed: () {
                              onBoardingProvider.nextPage(_pageController);
                            },
                            borderRadius: 30,
                            padding: EdgeInsets.symmetric(
                              horizontal: Dimensions.width192,
                            ),
                            child: const Text(
                              "Next",
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                              ),
                            ),
                          ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
