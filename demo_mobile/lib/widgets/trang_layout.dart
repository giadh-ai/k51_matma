import 'package:flutter/material.dart';

class TrangLayout extends StatelessWidget {
  const TrangLayout({
    required this.statusTitle,
    required this.statusMessage,
    required this.child,
    super.key,
  });

  final String statusTitle;
  final String statusMessage;
  final Widget child;

  static const _background = Color(0xFFF5F4F9);
  static const _red = Color(0xFFB32D36);

  @override
  Widget build(BuildContext context) {
    return ColoredBox(
      color: _background,
      child: SingleChildScrollView(
        child: Column(
          children: [
            Stack(
              clipBehavior: Clip.none,
              children: [
                Container(
                  height: 236,
                  color: _red,
                  child: SafeArea(
                    bottom: false,
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(20, 12, 20, 0),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Container(
                            width: 48,
                            height: 48,
                            alignment: Alignment.center,
                            decoration: BoxDecoration(
                              color: const Color(0xFFFFCF22),
                              shape: BoxShape.circle,
                              border: Border.all(color: Colors.white, width: 3),
                            ),
                            child: const Text(
                              'G',
                              style: TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.w800,
                                fontSize: 24,
                              ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          const Expanded(
                            child: Padding(
                              padding: EdgeInsets.only(top: 6),
                              child: Text(
                                'Xin chào, Đinh Hoàng Gia',
                                maxLines: 2,
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 19,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                            ),
                          ),
                          Container(
                            width: 48,
                            height: 48,
                            decoration: BoxDecoration(
                              color: const Color(0x29FFFFFF),
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: const Color(0x29FFFFFF),
                              ),
                            ),
                            child: const Icon(
                              Icons.notifications,
                              color: Colors.white,
                              size: 25,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                Positioned(
                  left: 16,
                  right: 16,
                  bottom: -70,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 17,
                      vertical: 18,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0x0F000000),
                          blurRadius: 16,
                          offset: const Offset(0, 5),
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        const SizedBox(
                          width: 68,
                          height: 68,
                          child: Stack(
                            alignment: Alignment.center,
                            children: [
                              Icon(
                                Icons.calendar_month_rounded,
                                size: 58,
                                color: Color(0xFF1689E8),
                              ),
                              Positioned(
                                right: 1,
                                bottom: 3,
                                child: Icon(
                                  Icons.check_circle,
                                  size: 23,
                                  color: Color(0xFF1887E4),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 12),
                        Container(
                          height: 64,
                          width: 1,
                          color: const Color(0xFFE7E8EC),
                        ),
                        const SizedBox(width: 13),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                statusTitle,
                                style: const TextStyle(
                                  color: Color(0xFF566174),
                                  fontSize: 19,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                statusMessage,
                                style: const TextStyle(
                                  color: Color(0xFF252B3A),
                                  fontSize: 15,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 94),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
              child: child,
            ),
          ],
        ),
      ),
    );
  }
}
