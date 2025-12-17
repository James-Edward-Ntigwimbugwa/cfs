import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:toastification/toastification.dart';

import '../../../../core/constants/dimensions.dart';
import '../../../../core/mixins/app_theme_mixin.dart';
import '../../../../shared/widgets/custom_button.dart';
import '../../../../shared/widgets/custom_text.dart';
import '../../../../shared/widgets/custom_text_form_field.dart';
import '../../routes/authentication_paths.dart';
import '../providers/auth_provider.dart';

class Login extends StatefulWidget {
  const Login({super.key});

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> with AppThemeMixin {
  final usernameController = TextEditingController(text: 'pmouser@pmo.go.tz');
  final passwordController = TextEditingController(text: '!Pmo@123');
  final _formKey = GlobalKey<FormState>();
  bool obscureText = true;

  @override
  void dispose() {
    usernameController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  String? _validateUsername(String? value) {
    if (value == null || value.isEmpty) {
      return 'Username is required';
    }
    if (value.length < 3) {
      return 'Username must be at least 3 characters';
    }
    return null;
  }

  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    }
    if (value.length < 6) {
      return 'Password must be at least 6 characters';
    }
    return null;
  }

  Future<void> _handleLogin(AuthProvider authProvider) async {
    if (_formKey.currentState?.validate() ?? false) {
      await authProvider.login(
        username: usernameController.text,
        password: passwordController.text,
      );

      if (mounted) {
        if (authProvider.isLoggedIn) {
          authProvider.isLoading = true;
          authProvider.isLoading = false;
        } else {
          toastification.show(
            type: ToastificationType.error,
            autoCloseDuration: const Duration(seconds: 3),
            title: CustomText(text: "Log in failed"),
            description: CustomText(text: authProvider.message),
          );
        }
      }
    } else {
      toastification.show(
        type: ToastificationType.error,
        autoCloseDuration: const Duration(seconds: 3),
        title: CustomText(text: "Validation Error"),
        description: CustomText(text: "Please fix all fields correctly!"),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    Dimensions.init(context);

    return Consumer<AuthProvider>(
      builder: (context, authProvider, child) {
        return Scaffold(
          backgroundColor: colorScheme.surface,
          body: SafeArea(
            child: CustomScrollView(
              physics: const BouncingScrollPhysics(),
              slivers: [
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
                          
                          // Logo/Brand Section
                          Center(
                            child: Container(
                              width: 120,
                              height: 120,
                              decoration: BoxDecoration(
                                color: colorScheme.primaryContainer,
                                shape: BoxShape.circle,
                              ),
                              child: Icon(
                                Icons.person_rounded,
                                size: 60,
                                color: colorScheme.primary,
                              ),
                            ),
                          ),
                          
                          SizedBox(height: Dimensions.height32),
                          
                          // Welcome Text
                          Center(
                            child: Text(
                              'Welcome Back',
                              style: textTheme.displaySmall?.copyWith(
                                fontWeight: FontWeight.bold,
                                color: colorScheme.onSurface,
                              ),
                            ),
                          ),
                          SizedBox(height: Dimensions.height8),
                          Center(
                            child: Text(
                              'Sign in to continue to Kiongozi App',
                              textAlign: TextAlign.center,
                              style: textTheme.bodyLarge?.copyWith(
                                color: colorScheme.onSurfaceVariant,
                              ),
                            ),
                          ),
                          
                          SizedBox(height: Dimensions.height48),
                          
                          // Username Field
                          Text(
                            'Username',
                            style: textTheme.labelLarge?.copyWith(
                              color: colorScheme.onSurface,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          SizedBox(height: Dimensions.height8),
                          CustomInputField(
                            hintText: 'Enter your username',
                            validator: _validateUsername,
                            controller: usernameController,
                            prefixIcon: Icon(
                              Icons.person_outline_rounded,
                              color: colorScheme.primary,
                            ),
                          ),
                          
                          SizedBox(height: Dimensions.height20),
                          
                          // Password Field
                          Text(
                            'Password',
                            style: textTheme.labelLarge?.copyWith(
                              color: colorScheme.onSurface,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          SizedBox(height: Dimensions.height8),
                          CustomInputField(
                            hintText: 'Enter your password',
                            controller: passwordController,
                            obscureText: obscureText,
                            validator: _validatePassword,
                            prefixIcon: Icon(
                              Icons.lock_outline_rounded,
                              color: colorScheme.primary,
                            ),
                            suffix: IconButton(
                              icon: Icon(
                                obscureText
                                    ? Icons.visibility_outlined
                                    : Icons.visibility_off_outlined,
                                color: colorScheme.onSurfaceVariant,
                              ),
                              onPressed: () {
                                setState(() {
                                  obscureText = !obscureText;
                                });
                              },
                            ),
                          ),
                          
                          SizedBox(height: Dimensions.height12),
                          
                          // Forgot Password
                          Align(
                            alignment: Alignment.centerRight,
                            child: TextButton(
                              onPressed: () {
                                context.push(AuthenticationPaths.forgotPassword);
                              },
                              child: Text(
                                'Forgot Password?',
                                style: textTheme.bodyMedium?.copyWith(
                                  color: colorScheme.primary,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ),
                          ),
                          
                          SizedBox(height: Dimensions.height24),
                          
                          // Sign In Button
                          SizedBox(
                            width: double.infinity,
                            height: Dimensions.height56,
                            child: CustomButton(
                              onPressed: authProvider.isLoading
                                  ? () {}
                                  : () => _handleLogin(authProvider),
                              child: authProvider.isLoading
                                  ? SizedBox(
                                      height: 24,
                                      width: 24,
                                      child: CircularProgressIndicator(
                                        color: colorScheme.onPrimary,
                                        strokeWidth: 2,
                                      ),
                                    )
                                  : CustomText(
                                      text: 'Sign In',
                                      style: textTheme.titleMedium?.copyWith(
                                        fontWeight: FontWeight.bold,
                                        color: colorScheme.onPrimary,
                                      ),
                                    ),
                            ),
                          ),
                          
                          SizedBox(height: Dimensions.height16),
                          
                          // Divider with "OR"
                          Row(
                            children: [
                              Expanded(
                                child: Divider(
                                  color: colorScheme.outlineVariant,
                                  thickness: 1,
                                ),
                              ),
                              Padding(
                                padding: EdgeInsets.symmetric(
                                  horizontal: Dimensions.width16,
                                ),
                                child: Text(
                                  'OR',
                                  style: textTheme.bodySmall?.copyWith(
                                    color: colorScheme.onSurfaceVariant,
                                  ),
                                ),
                              ),
                              Expanded(
                                child: Divider(
                                  color: colorScheme.outlineVariant,
                                  thickness: 1,
                                ),
                              ),
                            ],
                          ),
                          
                          SizedBox(height: Dimensions.height16),
                          
                          // Biometric Login Button (Optional)
                          SizedBox(
                            width: double.infinity,
                            height: Dimensions.height56,
                            child: OutlinedButton.icon(
                              onPressed: () {
                                // TODO: Implement biometric login
                              },
                              style: OutlinedButton.styleFrom(
                                side: BorderSide(
                                  color: colorScheme.outline,
                                  width: 1.5,
                                ),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(
                                    Dimensions.radius12,
                                  ),
                                ),
                              ),
                              icon: Icon(
                                Icons.fingerprint_rounded,
                                color: colorScheme.primary,
                              ),
                              label: Text(
                                'Sign in with Biometric',
                                style: textTheme.titleMedium?.copyWith(
                                  fontWeight: FontWeight.w600,
                                  color: colorScheme.onSurface,
                                ),
                              ),
                            ),
                          ),
                          
                          const Spacer(),
                          
                          // Sign Up Link
                          Center(
                            child: TextButton(
                              onPressed: () {
                                // TODO: Navigate to sign up
                              },
                              child: RichText(
                                text: TextSpan(
                                  text: "Don't have an account? ",
                                  style: textTheme.bodyMedium?.copyWith(
                                    color: colorScheme.onSurfaceVariant,
                                  ),
                                  children: [
                                    TextSpan(
                                      text: 'Sign Up',
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
      },
    );
  }
}