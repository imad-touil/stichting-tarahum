<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use App\Models\User;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        // التحقق من صحة البيانات
        $request->validate([
            'email' => 'required|email',
            'password' => 'required'
        ]);

        // البحث عن المستخدم
        $user = User::where('email', $request->email)->first();

        // التحقق من كلمة المرور
        if (!$user || !Hash::check($request->password, $user->password)) {
            return response()->json(['error' => 'Invalid credentials'], 401);
        }

        // إرجاع الدور (role)
        return response()->json([
            'message' => 'Login successful',
            'role' => $user->role
        ]);
    }
}
