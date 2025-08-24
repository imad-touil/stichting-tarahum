<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

// Add CORS headers for all routes
Route::middleware(['cors'])->group(function () {
    // Routes will be handled by API
});
