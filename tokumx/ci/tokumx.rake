require 'ci/common'

def tokumx_version
  ENV['FLAVOR_VERSION'] || '2.0.1'
end

def tokumx_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/tokumx_#{tokumx_version}"
end

namespace :ci do
  namespace :tokumx do |flavor|
    task before_install: ['ci:common:before_install']

    task install: ['ci:common:install'] do
      use_venv = in_venv
      install_requirements('tokumx/requirements.txt',
                           "--cache-dir #{ENV['PIP_CACHE']}",
                           "#{ENV['VOLATILE_DIR']}/ci.log", use_venv)
      sh %(bash tokumx/ci/start-docker.sh)
    end

    task before_script: ['ci:common:before_script']

    task :script, [:mocked] => ['ci:common:script'] do |_, attr|
      mocked = attr[:mocked] || false
      this_provides = [
        'tokumx'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides, mocked)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(bash tokumx/ci/stop-docker.sh)
    end

    task :execute, :mocked do |_, attr|
      mocked = attr[:mocked] || false
      exception = nil
      begin
        if not mocked
          %w(before_install install before_script).each do |u|
            Rake::Task["#{flavor.scope.path}:#{u}"].invoke
          end
        end
        Rake::Task["#{flavor.scope.path}:script"].invoke(mocked)
        Rake::Task["#{flavor.scope.path}:before_cache"].invoke
      rescue => e
        exception = e
        puts "Failed task: #{e.class} #{e.message}".red
      end
      if ENV['SKIP_CLEANUP']
        puts 'Skipping cleanup, disposable environments are great'.yellow
      else
        puts 'Cleaning up'
        Rake::Task["#{flavor.scope.path}:cleanup"].invoke
      end
      raise exception if exception
    end
  end
end
