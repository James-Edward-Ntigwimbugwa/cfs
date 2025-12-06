import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/constants/dimensions.dart';
import '../../../../core/mixins/app_theme_mixin.dart';
import '../../../../shared/widgets/custom_button.dart';
import '../../../../shared/widgets/custom_text.dart';
import '../../../../shared/widgets/custom_text_form_field.dart';
import '../../routes/authentication_paths.dart';

class ForgotPassword extends StatefulWidget {
  const ForgotPassword({super.key});

  @override
  State<ForgotPassword> createState() => _ForgotPasswordState();
}

class _ForgotPasswordState extends State<ForgotPassword> with AppThemeMixin {
  final _formKey = GlobalKey<FormState>();
  final usernameController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    usernameController.dispose();
    super.dispose();
  }

  String? _validateEmail(String? value) {
    if (value == null || value.isEmpty) {
      return 'Please enter your email or username';
    }

    // Check if it's an email format
    if (value.contains('@')) {
      final emailRegex = RegExp(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
      );
      if (!emailRegex.hasMatch(value)) {
        return 'Please enter a valid email address';
      }
    } else {
      // Username validation
      if (value.length < 3) {
        return 'Username must be at least 3 characters';
      }
    }

    return null;
  }

  Future<void> _handleResetPassword() async {
    if (_formKey.currentState?.validate() ?? false) {
      setState(() => _isLoading = true);

      // Simulate API call
      await Future.delayed(const Duration(seconds: 2));

      setState(() => _isLoading = false);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Text('Password reset link sent to your email'),
            backgroundColor: colorScheme.primary,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: colorScheme.surface,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // App Bar
            SliverAppBar(
              pinned: true,
              elevation: 0,
              backgroundColor: colorScheme.surface,
              leading: IconButton(
                icon: Icon(
                  Icons.arrow_back_ios_new,
                  color: colorScheme.onSurface,
                ),
                onPressed: () => context.pop(),
              ),
            ),

            // Content
            SliverFillRemaining(
              hasScrollBody: false,
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: Dimensions.width24),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Spacer(),

                      // Icon
                      Center(
                        child: Container(
                          width: 100,
                          height: 100,
                          decoration: BoxDecoration(
                            color: colorScheme.primaryContainer,
                            shape: BoxShape.circle,
                          ),
                          child: Icon(
                            Icons.lock_reset_rounded,
                            size: 50,
                            color: colorScheme.primary,
                          ),
                        ),
                      ),

                      SizedBox(height: Dimensions.height32),

                      // Header Section
                      Center(
                        child: Text(
                          'Forgot Password?',
                          style: textTheme.displaySmall?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: colorScheme.onSurface,
                          ),
                        ),
                      ),
                      SizedBox(height: Dimensions.height12),
                      Center(
                        child: Text(
                          'Enter your email or username and we\'ll send\nyou a link to reset your password',
                          textAlign: TextAlign.center,
                          style: textTheme.bodyLarge?.copyWith(
                            color: colorScheme.onSurfaceVariant,
                            height: 1.5,
                          ),
                        ),
                      ),

                      SizedBox(height: Dimensions.height48),

                      // Email/Username Field
                      Text(
                        'Email or Username',
                        style: textTheme.labelLarge?.copyWith(
                          color: colorScheme.onSurface,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      SizedBox(height: Dimensions.height8),
                      CustomInputField(
                        hintText: 'Enter your email or username',
                        validator: _validateEmail,
                        controller: usernameController,
                        keyboardType: TextInputType.emailAddress,
                        prefixIcon: Icon(
                          Icons.alternate_email_rounded,
                          color: colorScheme.primary,
                        ),
                      ),

                      SizedBox(height: Dimensions.height32),

                      // Reset Button
                      SizedBox(
                        width: double.infinity,
                        height: Dimensions.height56,
                        child: CustomButton(
                          onPressed: _isLoading
                              ? () {}
                              : () => _handleResetPassword(),
                          child: _isLoading
                              ? SizedBox(
                                  height: 24,
                                  width: 24,
                                  child: CircularProgressIndicator(
                                    color: colorScheme.onPrimary,
                                    strokeWidth: 2,
                                  ),
                                )
                              : CustomText(
                                  color: colorScheme.onPrimary,
                                  text: 'Send Reset Link',
                                  style: textTheme.titleMedium?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: colorScheme.onPrimary,
                                  ),
                                ),
                        ),
                      ),

                      const Spacer(),

                      // Sign In Link
                      Center(
                        child: TextButton(
                          onPressed: () =>
                              context.go(AuthenticationPaths.login),
                          child: RichText(
                            text: TextSpan(
                              text: 'Remember your password? ',
                              style: textTheme.bodyMedium?.copyWith(
                                color: colorScheme.onSurfaceVariant,
                              ),
                              children: [
                                TextSpan(
                                  text: 'Sign In',
                                  style: textTheme.bodyMedium?.copyWith(
                                    color: colorScheme.primary,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),

                      SizedBox(height: Dimensions.height24),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
