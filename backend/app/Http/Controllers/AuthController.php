<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Auth;
use App\Models\User;

class AuthController extends Controller
{
    public function __construct()
    {
        // Add CORS headers to all responses
        header('Access-Control-Allow-Origin: *');
        header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
        header('Access-Control-Allow-Headers: Content-Type, Authorization');
    }

    public function login(Request $request)
    {
        // Handle preflight OPTIONS request
        if ($request->getMethod() === 'OPTIONS') {
            return response()->json(['status' => 'OK'], 200);
        }

        // التحقق من صحة البيانات
        try {
            $request->validate([
                'email' => 'required|email',
                'password' => 'required'
            ]);
        } catch (\Illuminate\Validation\ValidationException $e) {
            return response()->json([
                'error' => 'Validation failed',
                'messages' => $e->errors()
            ], 422);
        }

        // البحث عن المستخدم
        $user = User::where('email', $request->email)->first();

        // التحقق من كلمة المرور
        if (!$user || !Hash::check($request->password, $user->password)) {
            return response()->json(['error' => 'Invalid credentials'], 401);
        }

        // Create session
        Auth::login($user);

        // إرجاع الدور (role) مع معلومات إضافية
        return response()->json([
            'message' => 'Login successful',
            'role' => $user->role,
            'name' => $user->name,
            'email' => $user->email
        ]);
    }

    public function logout(Request $request)
    {
        Auth::logout();
        return response()->json(['message' => 'Logout successful']);
    }

    public function user(Request $request)
    {
        if (Auth::check()) {
            $user = Auth::user();
            return response()->json([
                'user' => [
                    'name' => $user->name,
                    'email' => $user->email,
                    'role' => $user->role
                ]
            ]);
        }
        return response()->json(['error' => 'Not authenticated'], 401);
    }
}
