// ignore_for_file: file_names

import 'package:flutter/material.dart';

import 'widgets/trang_layout.dart';

class Trang1 extends StatelessWidget {
  const Trang1({super.key});

  @override
  Widget build(BuildContext context) {
    return TrangLayout(
      statusTitle: 'Lịch hôm nay:',
      statusMessage: 'Không tìm thấy lịch cá nhân',
      child: const _ChucNang(),
    );
  }
}

class _ChucNang extends StatelessWidget {
  const _ChucNang();

  static const _items = [
    (Icons.notifications_active_outlined, 'Thông báo', Color(0xFFE53950)),
    (Icons.mark_email_unread_outlined, 'Hộp thư', Color(0xFF1689E8)),
    (Icons.calendar_month_outlined, 'Lịch công tác', Color(0xFFFF9866)),
    (Icons.event_available_outlined, 'Lịch giảng dạy/\ncoi thi', Color(0xFFE53950)),
    (Icons.pause_circle_filled_rounded, 'Đề xuất tạm\nngưng', Color(0xFFFFC42E)),
    (Icons.co_present_rounded, 'Đề xuất dạy bù', Color(0xFF14A98A)),
  ];

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Container(
              width: 5,
              height: 34,
              decoration: BoxDecoration(
                color: const Color(0xFF1689E8),
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            const SizedBox(width: 12),
            const Expanded(
              child: Text(
                'Chức năng',
                style: TextStyle(
                  color: Color(0xFF222638),
                  fontSize: 22,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            OutlinedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.tune, size: 19),
              label: const Text('Tùy chỉnh'),
              style: OutlinedButton.styleFrom(
                foregroundColor: const Color(0xFF273044),
                side: const BorderSide(color: Color(0xFFE2E6EF)),
                backgroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 22),
        GridView.builder(
          itemCount: _items.length,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            mainAxisExtent: 128,
            crossAxisSpacing: 8,
          ),
          itemBuilder: (context, index) {
            final item = _items[index];
            return Column(
              children: [
                Container(
                  width: 72,
                  height: 72,
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(item.$1, size: 38, color: item.$3),
                ),
                const SizedBox(height: 9),
                Text(
                  item.$2,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Color(0xFF202638),
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    height: 1.3,
                  ),
                ),
              ],
            );
          },
        ),
        const SizedBox(height: 4),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 27,
              height: 7,
              decoration: BoxDecoration(
                color: const Color(0xFF1689E8),
                borderRadius: BorderRadius.circular(10),
              ),
            ),
            const SizedBox(width: 9),
            const CircleAvatar(radius: 4, backgroundColor: Color(0xFF8DC9F2)),
          ],
        ),
      ],
    );
  }
}
