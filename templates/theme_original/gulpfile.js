var gulp = require('gulp');
var sass = require('gulp-sass');
var browserSync = require('browser-sync').create();
var header = require('gulp-header');
var cleanCSS = require('gulp-clean-css');
var pug = require('gulp-pug');
var rename = require("gulp-rename");
var uglify = require('gulp-uglify');
var beautify = require('gulp-html-beautify');
var pkg = require('./package.json');
var banner = ['\n',
  ''
].join('');
gulp.task('sass', function() {
  return gulp.src('scss/sb-admin.scss')
    .pipe(sass())
    .pipe(header(banner, {
      pkg: pkg
    }))
    .pipe(gulp.dest('css'))
    .pipe(browserSync.reload({
      stream: true
    }))
});
gulp.task('minify-css', ['sass'], function() {
  return gulp.src('css/sb-admin.css')
    .pipe(cleanCSS({
      compatibility: 'ie8'
    }))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest('css'))
    .pipe(browserSync.reload({
      stream: true
    }))
});
gulp.task('minify-js', function() {
  return gulp.src(['js*.js', '!js*.min.js'])
    .pipe(uglify())
    .pipe(header(banner, {
      pkg: pkg
    }))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest('js'))
    .pipe(browserSync.reload({
      stream: true
    }))
});
gulp.task('pug', function buildHTML() {
  return gulp.src('pug*',
      '!**/npm.js',
      '!**/bootstrap-theme.*',
      '!***.map',
      '!node_modules/font-awesome/.npmignore',
      '!node_modules/font-awesome*', ['sass']);
  gulp.watch('pug*', ['pug']);
  gulp.watch('css*.js', browserSync.reload);
});
